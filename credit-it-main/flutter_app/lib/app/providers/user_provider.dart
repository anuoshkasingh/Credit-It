import 'package:flutter/material.dart';
import '../models/user.dart';
import '../models/recommendation.dart';
import '../services/api_service.dart';

class UserProvider with ChangeNotifier {
  List<User> _users = [];
  User? _currentUser;
  List<CardRecommendation> _recommendations = [];
  String _selectedCategory = 'All';
  bool _isLoading = false;
  String? _errorMessage;

  List<User> get users => _users;
  User? get currentUser => _currentUser;
  List<CardRecommendation> get recommendations => _recommendations;
  String get selectedCategory => _selectedCategory;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  UserProvider() {
    init();
  }

  Future<void> init() async {
    _isLoading = true;
    notifyListeners();

    _users = await ApiService.fetchUsers();
    if (_users.isNotEmpty) {
      _currentUser = _users.firstWhere(
        (u) => u.userId == '001',
        orElse: () => _users.first,
      );
    }
    
    await loadRecommendations();
  }

  Future<void> switchUser(User user) async {
    if (_currentUser?.userId == user.userId) return;
    _currentUser = user;
    notifyListeners();
    await loadRecommendations();
  }

  Future<void> setCategoryFilter(String category) async {
    _selectedCategory = category;
    notifyListeners();
    await loadRecommendations();
  }

  Future<void> loadRecommendations() async {
    if (_currentUser == null) return;
    
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _recommendations = await ApiService.fetchRecommendations(
        _currentUser!.userId,
        category: _selectedCategory,
      );
    } catch (e) {
      _errorMessage = 'Failed to load recommendations: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
