import 'credit_card.dart';

class CardRecommendation {
  final CreditCard card;
  final double netAnnualValue;
  final double grossRewards;
  final double annualFee;
  final double effectiveAnnualFee;
  final String aiSummary;
  final String personalizedExplanation;
  final List<String> topContributingCategories;
  final Map<String, double> categoryContributions;

  CardRecommendation({
    required this.card,
    required this.netAnnualValue,
    required this.grossRewards,
    required this.annualFee,
    required this.effectiveAnnualFee,
    required this.aiSummary,
    required this.personalizedExplanation,
    required this.topContributingCategories,
    required this.categoryContributions,
  });

  factory CardRecommendation.fromJson(Map<String, dynamic> json) {
    final rawCard = json['raw_card'] ?? json;
    final cardObj = CreditCard.fromJson(rawCard);

    List<String> cats = [];
    if (json['top_contributing_categories'] != null) {
      cats = List<String>.from(json['top_contributing_categories']);
    }

    Map<String, double> catContribs = {};
    if (json['category_contributions'] != null) {
      final Map<String, dynamic> map = json['category_contributions'];
      map.forEach((key, value) {
        catContribs[key] = (value as num).toDouble();
      });
    }

    return CardRecommendation(
      card: cardObj,
      netAnnualValue: (json['net_annual_value'] as num?)?.toDouble() ?? 0.0,
      grossRewards: (json['gross_rewards'] as num?)?.toDouble() ?? 0.0,
      annualFee: (json['annual_fee'] as num?)?.toDouble() ?? 0.0,
      effectiveAnnualFee: (json['effective_annual_fee'] as num?)?.toDouble() ?? 0.0,
      aiSummary: json['ai_summary'] ?? '',
      personalizedExplanation: json['personalized_explanation'] ?? '',
      topContributingCategories: cats,
      categoryContributions: catContribs,
    );
  }
}
