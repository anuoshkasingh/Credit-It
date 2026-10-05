import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../screens/payment_history_screen.dart';

class QuickActionsGrid extends StatelessWidget {
  const QuickActionsGrid({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // 1. UPI Money Transfer Section
        Container(
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.04),
                blurRadius: 8,
                offset: const Offset(0, 2),
              )
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'UPI Money Transfer',
                style: TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.primaryBlue,
                ),
              ),
              const SizedBox(height: 14),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildActionItem(Icons.qr_code_scanner, 'Scan & Pay', color: AppTheme.primaryBlue),
                  _buildActionItem(Icons.contact_phone, 'To Mobile', color: Colors.indigo),
                  _buildActionItem(Icons.send, 'To UPI Apps', color: Colors.blue),
                  _buildActionItem(Icons.account_balance, 'To Bank A/c', color: Colors.teal),
                ],
              ),
              const Divider(height: 24, thickness: 0.8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildActionItem(
                    Icons.account_balance_wallet,
                    'Balance\n& History',
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => const PaymentHistoryScreen()),
                      );
                    },
                  ),
                  _buildActionItem(Icons.compare_arrows, 'To Self\nAccount'),
                  _buildActionItem(Icons.arrow_downward, 'Receive\nMoney'),
                  _buildActionItem(Icons.shield_outlined, 'UPI Lite\nInstant'),
                ],
              ),
            ],
          ),
        ),

        // 2. My Paytm Row
        Container(
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppTheme.borderLight),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'My Paytm Services',
                    style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppTheme.primaryBlue),
                  ),
                  Text(
                    '9958736314@paytm',
                    style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildSmallTile(Icons.account_balance_wallet_outlined, 'Paytm\nWallet'),
                  _buildSmallTile(Icons.credit_card, 'Paytm\nPostpaid'),
                  _buildSmallTile(Icons.card_giftcard, 'Refer\n& Earn'),
                  _buildSmallTile(Icons.monetization_on_outlined, 'Personal\nLoan'),
                ],
              ),
            ],
          ),
        ),

        // 3. Recharge & Bill Payments Section Header (Fixed Overflow with Expanded & Flexible)
        Container(
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppTheme.borderLight),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Recharge & Bill Payments',
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AppTheme.primaryBlue),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    SizedBox(height: 2),
                    Text(
                      'Electricity, Mobile, DTH, Water & Gas',
                      style: TextStyle(fontSize: 10.5, color: Colors.grey),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              ElevatedButton.icon(
                onPressed: () {},
                icon: const Icon(Icons.qr_code, size: 13),
                label: const Text('Scan Any QR', style: TextStyle(fontSize: 10.5, fontWeight: FontWeight.bold)),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                  backgroundColor: AppTheme.primaryBlue,
                  minimumSize: Size.zero,
                  tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                ),
              )
            ],
          ),
        )
      ],
    );
  }

  Widget _buildActionItem(IconData icon, String label, {Color color = AppTheme.primaryBlue, VoidCallback? onTap}) {
    return GestureDetector(
      onTap: onTap,
      behavior: HitTestBehavior.opaque,
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: color.withOpacity(0.08),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: color, size: 24),
          ),
          const SizedBox(height: 6),
          Text(
            label,
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: AppTheme.textDark),
          ),
        ],
      ),
    );
  }

  Widget _buildSmallTile(IconData icon, String label) {
    return Column(
      children: [
        Icon(icon, color: AppTheme.accentBlue, size: 22),
        const SizedBox(height: 4),
        Text(
          label,
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 10, color: AppTheme.textDark),
        )
      ],
    );
  }
}
