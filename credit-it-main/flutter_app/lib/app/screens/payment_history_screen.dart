import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/transaction_item.dart';
import '../providers/user_provider.dart';
import '../services/api_service.dart';
import '../widgets/floating_chatbot_widget.dart';
import '../theme/app_theme.dart';

class PaymentHistoryScreen extends StatefulWidget {
  const PaymentHistoryScreen({super.key});

  @override
  State<PaymentHistoryScreen> createState() => _PaymentHistoryScreenState();
}

class _PaymentHistoryScreenState extends State<PaymentHistoryScreen> {
  bool _isLoading = true;
  List<TransactionItem> _allTransactions = [];
  List<TransactionItem> _filteredTransactions = [];
  bool _isSearching = false;
  final TextEditingController _searchController = TextEditingController();

  String? _lastUserId;

  @override
  void initState() {
    super.initState();
    _searchController.addListener(_onSearchChanged);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final userProvider = Provider.of<UserProvider>(context);
    final currentUserId = userProvider.currentUser?.userId ?? '001';
    if (_lastUserId != currentUserId) {
      _lastUserId = currentUserId;
      _loadTransactionsForUser(currentUserId);
    }
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _loadTransactionsForUser(String userId) async {
    setState(() {
      _isLoading = true;
    });

    try {
      final txs = await ApiService.fetchTransactions(userId);
      if (mounted) {
        setState(() {
          _allTransactions = txs;
          _filteredTransactions = txs;
          _isLoading = false;
        });
        _onSearchChanged();
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _onSearchChanged() {
    final query = _searchController.text.trim().toLowerCase();
    if (query.isEmpty) {
      setState(() {
        _filteredTransactions = _allTransactions;
      });
    } else {
      setState(() {
        _filteredTransactions = _allTransactions.where((t) {
          final merchant = t.merchantName.toLowerCase();
          final category = t.category.toLowerCase();
          final subcat = t.subcategory.toLowerCase();
          final amountStr = t.amount.toString();
          return merchant.contains(query) ||
              category.contains(query) ||
              subcat.contains(query) ||
              amountStr.contains(query);
        }).toList();
      });
    }
  }

  // Group transactions by "Month Year" (e.g. "September 2026", "July 2026")
  Map<String, List<TransactionItem>> _groupTransactionsByMonth(List<TransactionItem> list) {
    final Map<String, List<TransactionItem>> grouped = {};
    for (var tx in list) {
      final key = _formatMonthYear(tx.transactionDate);
      if (!grouped.containsKey(key)) {
        grouped[key] = [];
      }
      grouped[key]!.add(tx);
    }
    return grouped;
  }

  String _formatMonthYear(DateTime dt) {
    final months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return '${months[dt.month - 1]} ${dt.year}';
  }

  String _formatDateTime(DateTime dt) {
    final months = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];
    final day = dt.day;
    final month = months[dt.month - 1];
    int hour = dt.hour;
    final minute = dt.minute.toString().padLeft(2, '0');
    final period = hour >= 12 ? 'PM' : 'AM';
    hour = hour % 12;
    if (hour == 0) hour = 12;
    final hourStr = hour.toString().padLeft(2, '0');
    return '$day $month, $hourStr:$minute $period';
  }

  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);
    final currentUser = userProvider.currentUser;

    final grouped = _groupTransactionsByMonth(_filteredTransactions);

    return FloatingChatbotWidget(
      child: Scaffold(
        backgroundColor: const Color(0xFFF4F6F9),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0.5,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppTheme.primaryBlue),
          onPressed: () => Navigator.pop(context),
        ),
        title: _isSearching
            ? TextField(
                controller: _searchController,
                autofocus: true,
                decoration: const InputDecoration(
                  hintText: 'Search merchant, category, amount...',
                  border: InputBorder.none,
                  hintStyle: TextStyle(fontSize: 14, color: Colors.grey),
                ),
                style: const TextStyle(fontSize: 15, color: AppTheme.textDark),
              )
            : const Text(
                'Payment History',
                style: TextStyle(
                  color: AppTheme.primaryBlue,
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                ),
              ),
        actions: [
          IconButton(
            icon: Icon(
              _isSearching ? Icons.close : Icons.search,
              color: AppTheme.primaryBlue,
            ),
            onPressed: () {
              setState(() {
                if (_isSearching) {
                  _isSearching = false;
                  _searchController.clear();
                } else {
                  _isSearching = true;
                }
              });
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                // Active User Indicator Banner
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  color: AppTheme.primaryBlue.withOpacity(0.06),
                  child: Row(
                    children: [
                      CircleAvatar(
                        radius: 12,
                        backgroundColor: AppTheme.primaryBlue,
                        child: Text(
                          currentUser?.initials ?? 'U',
                          style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'Showing transactions for ${currentUser?.name ?? "User"}',
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          color: AppTheme.primaryBlue,
                        ),
                      ),
                      const Spacer(),
                      IconButton(
                        icon: const Icon(Icons.refresh, size: 16, color: AppTheme.primaryBlue),
                        onPressed: () => _loadTransactionsForUser(currentUser?.userId ?? '001'),
                        padding: EdgeInsets.zero,
                        constraints: const BoxConstraints(),
                      ),
                    ],
                  ),
                ),

                // Transactions List grouped by Month
                Expanded(
                  child: _filteredTransactions.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.receipt_long, size: 60, color: Colors.grey.shade400),
                              const SizedBox(height: 12),
                              Text(
                                _isSearching ? 'No matching transactions found' : 'No transactions recorded',
                                style: TextStyle(fontSize: 14, color: Colors.grey.shade600),
                              ),
                            ],
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.only(bottom: 24),
                          itemCount: grouped.keys.length,
                          itemBuilder: (context, index) {
                            final monthYear = grouped.keys.elementAt(index);
                            final txList = grouped[monthYear]!;
                            final totalSpent = txList.fold<double>(0.0, (sum, item) => sum + item.amount);

                            return Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                // Month Section Header
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text(
                                        monthYear,
                                        style: const TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.bold,
                                          color: AppTheme.textDark,
                                        ),
                                      ),
                                      Row(
                                        children: [
                                          Column(
                                            crossAxisAlignment: CrossAxisAlignment.end,
                                            children: [
                                              const Text(
                                                'Total Spent',
                                                style: TextStyle(fontSize: 10.5, color: Colors.grey),
                                              ),
                                              Text(
                                                '₹${totalSpent.toStringAsFixed(0).replaceAllMapped(RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'), (Match m) => '${m[1]},')}',
                                                style: const TextStyle(
                                                  fontSize: 13,
                                                  fontWeight: FontWeight.bold,
                                                  color: AppTheme.textDark,
                                                ),
                                              ),
                                            ],
                                          ),
                                          const SizedBox(width: 4),
                                          const Icon(Icons.chevron_right, size: 18, color: Colors.blue),
                                        ],
                                      ),
                                    ],
                                  ),
                                ),

                                // Transaction Cards in Month
                                ...txList.map((tx) => _buildTransactionCard(tx)),
                              ],
                            );
                          },
                        ),
                ),
              ],
            ),
    ),
    );
  }

  Widget _buildTransactionCard(TransactionItem tx) {
    final merchantName = tx.merchantName;
    final category = tx.category;
    final dateStr = _formatDateTime(tx.transactionDate);
    final amountStr = '- ₹${tx.amount.toStringAsFixed(0).replaceAllMapped(RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'), (Match m) => '${m[1]},')}';

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 5),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.03),
            blurRadius: 6,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          // 1. Merchant / Category Logo Avatar
          _buildMerchantAvatar(merchantName, category),
          const SizedBox(width: 12),

          // 2. Merchant Name, Date & Category Tag
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  merchantName,
                  style: const TextStyle(
                    fontSize: 13.5,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textDark,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 3),
                Text(
                  dateStr,
                  style: TextStyle(
                    fontSize: 11,
                    color: Colors.grey.shade600,
                  ),
                ),
                const SizedBox(height: 6),
                _buildCategoryBadge(category),
              ],
            ),
          ),

          const SizedBox(width: 8),

          // 3. Amount & Payment Method Badge
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                amountStr,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.textDark,
                ),
              ),
              const SizedBox(height: 6),
              Row(
                children: [
                  const Text(
                    'From ',
                    style: TextStyle(fontSize: 10, color: Colors.grey),
                  ),
                  Container(
                    width: 14,
                    height: 14,
                    decoration: const BoxDecoration(
                      color: AppTheme.accentBlue,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      Icons.check,
                      size: 9,
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMerchantAvatar(String merchant, String category) {
    final mLower = merchant.toLowerCase();
    Color bg = const Color(0xFFE8F1FF);
    IconData icon = Icons.shopping_bag_outlined;

    if (mLower.contains('swiggy')) {
      bg = const Color(0xFFFFF0E6);
      icon = Icons.fastfood_outlined;
    } else if (mLower.contains('airtel') || mLower.contains('jio')) {
      bg = const Color(0xFFFFECEC);
      icon = Icons.receipt_long_outlined;
    } else if (mLower.contains('aakash') || category.toLowerCase().contains('education')) {
      bg = const Color(0xFFE5F6FF);
      icon = Icons.school_outlined;
    } else if (mLower.contains('ub') || category.toLowerCase().contains('travel')) {
      bg = const Color(0xFFF0F0F0);
      icon = Icons.directions_car_outlined;
    } else if (category.toLowerCase().contains('grocer')) {
      bg = const Color(0xFFEAFCEB);
      icon = Icons.shopping_cart_outlined;
    } else if (category.toLowerCase().contains('food') || category.toLowerCase().contains('dining')) {
      bg = const Color(0xFFFFF3E0);
      icon = Icons.restaurant_outlined;
    }

    return Container(
      width: 42,
      height: 42,
      decoration: BoxDecoration(
        color: bg,
        shape: BoxShape.circle,
      ),
      child: Icon(icon, color: AppTheme.primaryBlue, size: 20),
    );
  }

  Widget _buildCategoryBadge(String category) {
    final cLower = category.toLowerCase();
    String label = category;
    IconData icon = Icons.label_outline;

    if (cLower.contains('education')) {
      label = 'Education';
      icon = Icons.school_outlined;
    } else if (cLower.contains('grocer')) {
      label = 'Groceries';
      icon = Icons.shopping_cart_outlined;
    } else if (cLower.contains('bill') || cLower.contains('util')) {
      label = 'Bill Payments';
      icon = Icons.receipt_outlined;
    } else if (cLower.contains('food') || cLower.contains('dining')) {
      label = 'Food';
      icon = Icons.fastfood_outlined;
    } else if (cLower.contains('travel') || cLower.contains('flight')) {
      label = 'Travel';
      icon = Icons.flight_takeoff_outlined;
    } else if (cLower.contains('shop')) {
      label = 'Shopping';
      icon = Icons.shopping_bag_outlined;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: Colors.grey.shade100,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: Colors.grey.shade300, width: 0.6),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 10, color: Colors.grey.shade700),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 10,
              fontWeight: FontWeight.w500,
              color: Colors.grey.shade800,
            ),
          ),
        ],
      ),
    );
  }
}
