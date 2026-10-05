import 'package:shared_preferences/shared_preferences.dart';

class ApiKeyService {
  static const String _storageKey = 'gemini_api_key';
  static const String defaultApiKey = "";

  static String _currentKey = defaultApiKey;

  static String get apiKey => _currentKey;

  static Future<void> init() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedKey = prefs.getString(_storageKey);
      if (savedKey != null && savedKey.trim().isNotEmpty) {
        _currentKey = savedKey.trim();
      } else {
        _currentKey = defaultApiKey;
      }
    } catch (_) {
      _currentKey = defaultApiKey;
    }
  }

  static Future<bool> setApiKey(String newKey) async {
    final keyToSave = newKey.trim();
    if (keyToSave.isEmpty) return false;

    _currentKey = keyToSave;
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_storageKey, keyToSave);
      return true;
    } catch (_) {
      return true; // Still updated in-memory
    }
  }

  static Future<void> resetToDefault() async {
    _currentKey = defaultApiKey;
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove(_storageKey);
    } catch (_) {}
  }
}
