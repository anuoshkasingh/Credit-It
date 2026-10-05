class CreditCard {
  final String cardId;
  final String cardName;
  final String bankName;
  final String cardNetwork;
  final String cardType;
  final String imagePath;
  final String applyUrl;
  final double joiningFee;
  final double annualFee;
  final double annualFeeWaiverSpend;
  final double minimumIncome;
  final int minimumCreditScore;
  final String eligibilityNotes;
  final String rewardType;
  final double rewardRate;
  final double foodReward;
  final double shoppingReward;
  final double travelReward;
  final double fuelReward;
  final double groceryReward;
  final double utilityReward;
  final double onlineReward;
  final String welcomeBenefit;
  final String milestoneBenefit;
  final String loungeAccess;
  final String fuelSurchargeWaiver;
  final String diningBenefit;
  final String movieBenefit;

  CreditCard({
    required this.cardId,
    required this.cardName,
    required this.bankName,
    required this.cardNetwork,
    required this.cardType,
    required this.imagePath,
    this.applyUrl = '',
    required this.joiningFee,
    required this.annualFee,
    required this.annualFeeWaiverSpend,
    required this.minimumIncome,
    required this.minimumCreditScore,
    required this.eligibilityNotes,
    required this.rewardType,
    required this.rewardRate,
    required this.foodReward,
    required this.shoppingReward,
    required this.travelReward,
    required this.fuelReward,
    required this.groceryReward,
    required this.utilityReward,
    required this.onlineReward,
    required this.welcomeBenefit,
    required this.milestoneBenefit,
    required this.loungeAccess,
    required this.fuelSurchargeWaiver,
    required this.diningBenefit,
    required this.movieBenefit,
  });

  factory CreditCard.fromJson(Map<String, dynamic> json) {
    return CreditCard(
      cardId: json['card_id'] ?? '',
      cardName: json['card_name'] ?? '',
      bankName: json['bank_name'] ?? '',
      cardNetwork: json['card_network'] ?? 'Visa',
      cardType: json['card_type'] ?? 'Rewards',
      imagePath: json['image_path'] ?? '',
      applyUrl: json['apply_url'] ?? 'https://www.google.com/search?q=${Uri.encodeComponent(json['card_name'] ?? '')}',
      joiningFee: (json['joining_fee'] as num?)?.toDouble() ?? 0.0,
      annualFee: (json['annual_fee'] as num?)?.toDouble() ?? 0.0,
      annualFeeWaiverSpend: (json['annual_fee_waiver_spend'] as num?)?.toDouble() ?? 0.0,
      minimumIncome: (json['minimum_income'] as num?)?.toDouble() ?? 0.0,
      minimumCreditScore: (json['minimum_credit_score'] as num?)?.toInt() ?? 600,
      eligibilityNotes: json['eligibility_notes'] ?? '',
      rewardType: json['reward_type'] ?? 'Rewards',
      rewardRate: (json['reward_rate'] as num?)?.toDouble() ?? 1.0,
      foodReward: (json['food_reward'] as num?)?.toDouble() ?? 0.0,
      shoppingReward: (json['shopping_reward'] as num?)?.toDouble() ?? 0.0,
      travelReward: (json['travel_reward'] as num?)?.toDouble() ?? 0.0,
      fuelReward: (json['fuel_reward'] as num?)?.toDouble() ?? 0.0,
      groceryReward: (json['grocery_reward'] as num?)?.toDouble() ?? 0.0,
      utilityReward: (json['utility_reward'] as num?)?.toDouble() ?? 0.0,
      onlineReward: (json['online_reward'] as num?)?.toDouble() ?? 0.0,
      welcomeBenefit: json['welcome_benefit'] ?? 'N/A',
      milestoneBenefit: json['milestone_benefit'] ?? 'N/A',
      loungeAccess: json['lounge_access'] ?? 'N/A',
      fuelSurchargeWaiver: json['fuel_surcharge_waiver'] ?? 'N/A',
      diningBenefit: json['dining_benefit'] ?? 'N/A',
      movieBenefit: json['movie_benefit'] ?? 'N/A',
    );
  }

  String get assetPath {
    final filename = '$cardId.png';
    return 'assets/cards/$filename';
  }
}
