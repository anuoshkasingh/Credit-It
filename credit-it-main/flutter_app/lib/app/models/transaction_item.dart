class TransactionItem {
  final String transactionId;
  final String userId;
  final DateTime transactionDate;
  final String merchantName;
  final String category;
  final String subcategory;
  final double amount;
  final String paymentMethod;
  final String merchantType;
  final String frequencyType;

  TransactionItem({
    required this.transactionId,
    required this.userId,
    required this.transactionDate,
    required this.merchantName,
    required this.category,
    required this.subcategory,
    required this.amount,
    required this.paymentMethod,
    required this.merchantType,
    required this.frequencyType,
  });

  factory TransactionItem.fromJson(Map<String, dynamic> json) {
    return TransactionItem(
      transactionId: json['transaction_id'] ?? '',
      userId: json['user_id'] ?? '',
      transactionDate: DateTime.tryParse(json['transaction_date'] ?? '') ?? DateTime.now(),
      merchantName: json['merchant_name'] ?? '',
      category: json['category'] ?? '',
      subcategory: json['subcategory'] ?? '',
      amount: (json['amount'] as num?)?.toDouble() ?? 0.0,
      paymentMethod: json['payment_method'] ?? 'UPI',
      merchantType: json['merchant_type'] ?? 'Online',
      frequencyType: json['frequency_type'] ?? 'One-time',
    );
  }
}
