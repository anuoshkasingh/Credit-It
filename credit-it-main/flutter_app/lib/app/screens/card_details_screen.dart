import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/recommendation.dart';
import '../providers/chatbot_provider.dart';
import '../widgets/floating_chatbot_widget.dart';
import '../theme/app_theme.dart';

class CardDetailsScreen extends StatefulWidget {
  final CardRecommendation recommendation;

  const CardDetailsScreen({
    super.key,
    required this.recommendation,
  });

  @override
  State<CardDetailsScreen> createState() => _CardDetailsScreenState();
}

class _CardDetailsScreenState extends State<CardDetailsScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) {
        Provider.of<ChatbotProvider>(context, listen: false).setActiveCard(widget.recommendation);
      }
    });
  }

  Future<void> _launchOfficialApplyUrl(BuildContext context) async {
    final card = widget.recommendation.card;
    final Uri url = Uri.parse(card.applyUrl.isNotEmpty
        ? card.applyUrl
        : 'https://www.google.com/search?q=${Uri.encodeComponent("${card.bankName} ${card.cardName} apply")}');

    try {
      final bool launched = await launchUrl(url, mode: LaunchMode.externalApplication);
      if (!launched) {
        await launchUrl(url, mode: LaunchMode.inAppWebView);
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Opening official portal: ${card.applyUrl}'),
            backgroundColor: AppTheme.primaryBlue,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final card = widget.recommendation.card;

    return PopScope(
      onPopInvokedWithResult: (didPop, result) {
        Provider.of<ChatbotProvider>(context, listen: false).clearActiveCard();
      },
      child: FloatingChatbotWidget(
        child: Scaffold(
          backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        foregroundColor: AppTheme.primaryBlue,
        elevation: 0,
        title: Text(
          card.cardName,
          style: const TextStyle(
            color: AppTheme.primaryBlue,
            fontWeight: FontWeight.bold,
            fontSize: 17,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.help_outline, color: AppTheme.primaryBlue),
            onPressed: () {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. Top Card Image & Banner Section (Light White-Blue Theme)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(vertical: 24, horizontal: 20),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    AppTheme.primaryBlue.withOpacity(0.05),
                    AppTheme.accentBlue.withOpacity(0.12),
                  ],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                ),
              ),
              child: Column(
                children: [
                  Container(
                    width: 260,
                    height: 160,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: AppTheme.primaryBlue.withOpacity(0.25),
                          blurRadius: 16,
                          offset: const Offset(0, 8),
                        ),
                      ],
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(16),
                      child: Image.asset(
                        card.assetPath,
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) {
                          return Container(
                            decoration: BoxDecoration(
                              gradient: const LinearGradient(
                                colors: [AppTheme.primaryBlue, AppTheme.accentBlue],
                              ),
                              borderRadius: BorderRadius.circular(16),
                            ),
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      card.bankName,
                                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                                    ),
                                    const Icon(Icons.contactless, color: Colors.white70),
                                  ],
                                ),
                                Text(
                                  card.cardName,
                                  style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                                ),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    const Text('**** **** **** 4892', style: TextStyle(color: Colors.white70)),
                                    Text(card.cardNetwork, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                                  ],
                                )
                              ],
                            ),
                          );
                        },
                      ),
                    ),
                  ),

                  const SizedBox(height: 16),

                  Text(
                    card.cardName,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primaryBlue,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),

                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      _buildHeaderTag(card.annualFee == 0 ? 'ZERO JOINING FEE' : 'FIRST YEAR FREE'),
                      const SizedBox(width: 8),
                      _buildHeaderTag('LIMITED TIME OFFER'),
                    ],
                  ),

                  const SizedBox(height: 12),

                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    decoration: BoxDecoration(
                      color: AppTheme.greenPositive.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppTheme.greenPositive.withOpacity(0.3)),
                    ),
                    child: Text(
                      'Estimated Net Value: +₹${widget.recommendation.netAnnualValue.toStringAsFixed(0)} / year',
                      style: const TextStyle(
                        color: AppTheme.greenPositive,
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                      ),
                    ),
                  )
                ],
              ),
            ),

            const SizedBox(height: 16),

            // 2. Key Features & Benefits Section
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Key Features & Benefits',
                    style: TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primaryBlue,
                    ),
                  ),
                  const SizedBox(height: 14),

                  _buildBenefitRow(
                    '${card.rewardRate}% base reward rate on spends',
                    'recharges, bill payments, shopping, flights, hotels & more*',
                    Icons.star_outline,
                  ),
                  _buildBenefitRow(
                    'Higher reward multipliers on online spends',
                    'including brands like Amazon, Swiggy, Zomato, Uber & Myntra*',
                    Icons.shopping_bag_outlined,
                  ),
                  _buildBenefitRow(
                    'Lounge Access & Travel Benefits',
                    card.loungeAccess != 'N/A' ? card.loungeAccess : 'Complimentary lounge access at major airports',
                    Icons.flight_takeoff,
                  ),
                  _buildBenefitRow(
                    'Fuel Surcharge Waiver',
                    card.fuelSurchargeWaiver != 'N/A' ? card.fuelSurchargeWaiver : '1% waiver across all fuel stations in India*',
                    Icons.local_gas_station_outlined,
                  ),
                ],
              ),
            ),

            const Divider(height: 32, thickness: 1, indent: 20, endIndent: 20),

            // 3. AI Personalized Explanation Section (FIXED OVERFLOW ISSUE: Page 1 Item 3)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppTheme.primaryBlue.withOpacity(0.04),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppTheme.primaryBlue.withOpacity(0.15)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Fixed overflow: Wrapped Text in Expanded inside Row
                    const Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Icon(Icons.psychology, color: AppTheme.primaryBlue, size: 22),
                        SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            'Why Gemini AI Recommended This Card',
                            style: TextStyle(
                              fontSize: 14.5,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.primaryBlue,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      widget.recommendation.personalizedExplanation,
                      style: const TextStyle(
                        fontSize: 13,
                        color: AppTheme.textDark,
                        height: 1.5,
                      ),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 24),

            // 4. Apply Now Section (Direct Official Bank Link - Page 5 Item 5)
            Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 10,
                    offset: Offset(0, -4),
                  )
                ],
              ),
              child: Column(
                children: [
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.primaryBlue,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      onPressed: () => _launchOfficialApplyUrl(context),
                      icon: const Icon(Icons.open_in_new, size: 18),
                      label: const Text(
                        'Apply Now on Official Bank Site',
                        style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    ),
    ),
    );
  }

  Widget _buildHeaderTag(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: AppTheme.primaryBlue,
        borderRadius: BorderRadius.circular(6),
      ),
      child: Text(
        text,
        style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _buildBenefitRow(String title, String subtitle, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: AppTheme.accentBlue.withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: AppTheme.primaryBlue, size: 20),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textDark,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  subtitle,
                  style: const TextStyle(
                    fontSize: 12,
                    color: AppTheme.textSecondary,
                  ),
                ),
              ],
            ),
          )
        ],
      ),
    );
  }
}
