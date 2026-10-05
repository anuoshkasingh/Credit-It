import 'package:flutter/material.dart';
import '../models/chat_message.dart';
import '../models/credit_card.dart';
import '../models/recommendation.dart';
import '../services/api_service.dart';
import '../services/chatbot_service.dart';
import 'user_provider.dart';

class ChatbotProvider with ChangeNotifier {
  bool _isOpen = false;
  bool _isLoading = false;
  CardRecommendation? _activeCardRec;
  List<CreditCard>? _comparisonCards;

  final List<ChatMessage> _messages = [
    ChatMessage(
      text: "Hi! 👋 I'm your Credit It Assistant. Ask me anything about your credit card recommendations, reward benefits, or card comparisons!",
      isUser: false,
      timestamp: DateTime.now(),
    ),
  ];

  bool get isOpen => _isOpen;
  bool get isLoading => _isLoading;
  List<ChatMessage> get messages => List.unmodifiable(_messages);
  CardRecommendation? get activeCardRec => _activeCardRec;
  List<CreditCard>? get comparisonCards => _comparisonCards;

  void openPanel() {
    _isOpen = true;
    notifyListeners();
  }

  void closePanel() {
    _isOpen = false;
    notifyListeners();
  }

  void togglePanel() {
    _isOpen = !_isOpen;
    notifyListeners();
  }

  void setActiveCard(CardRecommendation? rec) {
    if (_activeCardRec != rec) {
      _activeCardRec = rec;
      notifyListeners();
    }
  }

  void clearActiveCard() {
    if (_activeCardRec != null) {
      _activeCardRec = null;
      notifyListeners();
    }
  }

  void setActiveComparison(List<CreditCard>? cards) {
    _comparisonCards = cards;
    notifyListeners();
  }

  Future<void> sendMessage(String text, UserProvider userProvider) async {
    final query = text.trim();
    if (query.isEmpty || _isLoading) return;

    final user = userProvider.currentUser;
    if (user == null) return;

    final userMsg = ChatMessage(
      text: query,
      isUser: true,
      timestamp: DateTime.now(),
      contextLabel: _activeCardRec?.card.cardName,
    );

    _messages.add(userMsg);
    _isLoading = true;
    notifyListeners();

    try {
      final txs = await ApiService.fetchTransactions(user.userId);

      final responseText = await ChatbotService.generateResponse(
        userQuery: query,
        user: user,
        transactions: txs,
        activeCardRec: _activeCardRec,
        comparisonCards: _comparisonCards,
        currentRecommendations: userProvider.recommendations,
      );

      final isLimitError = responseText.contains("limit reached") || responseText.contains("Invalid Gemini API key");

      _messages.add(
        ChatMessage(
          text: responseText,
          isUser: false,
          timestamp: DateTime.now(),
          isError: isLimitError,
        ),
      );
    } catch (e) {
      _messages.add(
        ChatMessage(
          text: "An error occurred while generating response. Please check your internet connection.",
          isUser: false,
          timestamp: DateTime.now(),
          isError: true,
        ),
      );
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearChat() {
    _messages.clear();
    _activeCardRec = null;
    _comparisonCards = null;
    _messages.add(
      ChatMessage(
        text: "Hi! 👋 I'm your Credit It Assistant. Ask me anything about your credit card recommendations, reward benefits, or card comparisons!",
        isUser: false,
        timestamp: DateTime.now(),
      ),
    );
    notifyListeners();
  }
}
