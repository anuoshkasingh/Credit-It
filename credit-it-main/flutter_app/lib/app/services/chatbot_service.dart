import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/credit_card.dart';
import '../models/recommendation.dart';
import '../models/user.dart';
import '../models/transaction_item.dart';
import 'api_key_service.dart';

class ChatbotService {
  static const List<String> _models = [
    'gemini-1.5-flash',
    'gemini-2.0-flash',
    'gemini-2.5-flash',
    'gemini-3.6-flash'
  ];

  static Future<String> generateResponse({
    required String userQuery,
    required User user,
    List<TransactionItem>? transactions,
    CardRecommendation? activeCardRec,
    List<CreditCard>? comparisonCards,
    List<CardRecommendation>? currentRecommendations,
  }) async {
    final apiKey = ApiKeyService.apiKey;
    if (apiKey.isEmpty) {
      return "Gemini API key is missing. Please set your key in Profile → API Settings.";
    }

    final prompt = _buildPrompt(
      userQuery: userQuery,
      user: user,
      transactions: transactions,
      activeCardRec: activeCardRec,
      comparisonCards: comparisonCards,
      currentRecommendations: currentRecommendations,
    );

    // Try primary and fallback Gemini model endpoints
    for (String model in _models) {
      try {
        final url = Uri.parse(
          'https://generativelanguage.googleapis.com/v1beta/models/$model:generateContent?key=$apiKey',
        );

        final response = await http.post(
          url,
          headers: {'Content-Type': 'application/json'},
          body: json.encode({
            'contents': [
              {
                'role': 'user',
                'parts': [{'text': prompt}]
              }
            ],
            'generationConfig': {
              'temperature': 0.7,
              'maxOutputTokens': 2500,
            }
          }),
        ).timeout(const Duration(seconds: 12));

        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          final candidates = data['candidates'] as List?;
          if (candidates != null && candidates.isNotEmpty) {
            final parts = candidates[0]['content']?['parts'] as List?;
            if (parts != null && parts.isNotEmpty) {
              final text = parts[0]['text'] as String?;
              if (text != null && text.trim().isNotEmpty) {
                return _cleanMarkdown(text.trim());
              }
            }
          }
        } else if (response.statusCode == 429) {
          return "Gemini API limit reached. You can update your API key in Profile → API Settings.";
        } else if (response.statusCode == 400 || response.statusCode == 401 || response.statusCode == 403) {
          return "Invalid Gemini API key. Please check or update your key in Profile → API Settings.";
        }
      } catch (e) {
        // Continue to next model if network error or timeout
      }
    }

    return "Unable to connect to Gemini AI right now. Please verify your internet connection or update your API key in Profile → API Settings.";
  }

  static String _cleanMarkdown(String text) {
    var cleaned = text;

    // 1. Remove horizontal rules (--- or *** or ___)
    cleaned = cleaned.replaceAll(RegExp(r'^\s*[-*_]{3,}\s*$', multiLine: true), '');

    // 2. Remove markdown header tags (###, ##, #)
    cleaned = cleaned.replaceAll(RegExp(r'^\s*#+\s*', multiLine: true), '');

    // 3. Remove bold and italic formatting (**word**, *word*, __word__, _word_)
    cleaned = cleaned.replaceAll(RegExp(r'\*\*([^*]+)\*\*'), r'$1');
    cleaned = cleaned.replaceAll(RegExp(r'\*([^*]+)\*'), r'$1');
    cleaned = cleaned.replaceAll(RegExp(r'__([^_]+)__'), r'$1');
    cleaned = cleaned.replaceAll(RegExp(r'_([^_]+)_'), r'$1');

    // 4. Convert list bullets (*, -, +) at start of line to neat bullet symbol (•)
    cleaned = cleaned.replaceAll(RegExp(r'^\s*[*+-]\s+', multiLine: true), '• ');

    // 5. Cleanup any stray asterisks or hashes left behind
    cleaned = cleaned.replaceAll('**', '').replaceAll('#', '');

    // 6. Clean up multiple empty lines
    cleaned = cleaned.replaceAll(RegExp(r'\n{3,}'), '\n\n');

    return cleaned.trim();
  }

  static String _buildPrompt({
    required String userQuery,
    required User user,
    List<TransactionItem>? transactions,
    CardRecommendation? activeCardRec,
    List<CreditCard>? comparisonCards,
    List<CardRecommendation>? currentRecommendations,
  }) {
    final sb = StringBuffer();

    sb.writeln("SYSTEM INSTRUCTIONS:");
    sb.writeln("You are 'Credit It Assistant', a friendly, financial-expert AI assistant built into the Credit-It mobile app.");
    sb.writeln("Your role is to help ${user.name} understand credit card recommendations, compare cards, explain reward benefits, and clarify financial terms.");
    sb.writeln("CRITICAL RULES:");
    sb.writeln("1. Give personalized, clear, concise explanations tailored to the user's actual spending pattern.");
    sb.writeln("2. Do NOT invent card features, rewards, or fees not present in the provided local context.");
    sb.writeln("3. Explain complex financial terminology (like lounge access, 5X rewards, annual fee waiver) in simple, easy-to-understand language.");
    sb.writeln("4. Provide complete, fully detailed explanations without stopping mid-sentence or cutting off formatting.");
    sb.writeln("5. Output PLAIN TEXT ONLY. Do NOT use Markdown syntax such as headers (###), bold syntax (**text**), or horizontal lines (---). Use simple bullet points (•) and clear paragraph spacing.");

    sb.writeln("\n--- USER PROFILE & SPENDING CONTEXT ---");
    sb.writeln("User Name: ${user.name}");
    sb.writeln("User ID: ${user.userId}");

    if (user.userId == "001") {
      sb.writeln("Profile: High-income professional (~₹18 Lakhs annual income, ₹14 Lakhs annual spend). Major spending in Travel, Hotels, Luxury Shopping, Fine Dining.");
    } else if (user.userId == "002") {
      sb.writeln("Profile: Mid-income family spender (~₹5.5 Lakhs annual income, ₹3 Lakhs annual spend). Major spending in D-Mart Groceries, Swiggy Food, Airtel Utilities, Myntra.");
    } else {
      sb.writeln("Profile: Student / Youth (~₹1.8 Lakhs income, ₹75k spend). Major spending in Campus Food, Mobile Recharges, Metro Rail, Zepto, Movies.");
    }

    if (transactions != null && transactions.isNotEmpty) {
      sb.writeln("\nRecent Sample Transactions:");
      final sample = transactions.take(5);
      for (var t in sample) {
        sb.writeln("- ${t.merchantName} (${t.category}): ₹${t.amount.toStringAsFixed(0)} via ${t.paymentMethod}");
      }
    }

    if (activeCardRec != null) {
      final card = activeCardRec.card;
      sb.writeln("\n--- CURRENTLY VIEWED CARD CONTEXT ---");
      sb.writeln("Card Name: ${card.cardName}");
      sb.writeln("Bank: ${card.bankName} | Network: ${card.cardNetwork} | Type: ${card.cardType}");
      sb.writeln("Annual Fee: ₹${card.annualFee.toStringAsFixed(0)} (Waiver spend: ₹${card.annualFeeWaiverSpend.toStringAsFixed(0)})");
      sb.writeln("Estimated Net Annual Savings for user: +₹${activeCardRec.netAnnualValue.toStringAsFixed(0)}/year");
      sb.writeln("Reward Rate: ${card.rewardRate}% (${card.rewardType})");
      sb.writeln("Key Benefits: Welcome: ${card.welcomeBenefit} | Lounge: ${card.loungeAccess} | Dining: ${card.diningBenefit} | Fuel: ${card.fuelSurchargeWaiver}");
      sb.writeln("AI Reasoning Summary: ${activeCardRec.aiSummary}");
    }

    if (comparisonCards != null && comparisonCards.isNotEmpty) {
      sb.writeln("\n--- CARDS IN COMPARISON ---");
      for (var card in comparisonCards) {
        sb.writeln("- ${card.cardName} (${card.bankName}): Fee ₹${card.annualFee.toStringAsFixed(0)}, Reward: ${card.rewardRate}% ${card.rewardType}, Lounge: ${card.loungeAccess}");
      }
    }

    if (currentRecommendations != null && currentRecommendations.isNotEmpty && activeCardRec == null) {
      sb.writeln("\n--- TOP RECOMMENDED CARDS FOR USER ---");
      for (var rec in currentRecommendations.take(3)) {
        sb.writeln("- ${rec.card.cardName}: Net Value +₹${rec.netAnnualValue.toStringAsFixed(0)}/yr (${rec.aiSummary})");
      }
    }

    sb.writeln("\n--- USER QUESTION ---");
    sb.writeln(userQuery);

    return sb.toString();
  }
}
