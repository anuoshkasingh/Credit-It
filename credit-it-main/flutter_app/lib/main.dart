import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'app/providers/user_provider.dart';
import 'app/providers/chatbot_provider.dart';
import 'app/services/api_key_service.dart';
import 'app/theme/app_theme.dart';
import 'app/screens/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await ApiKeyService.init();
  runApp(const CreditItApp());
}

class CreditItApp extends StatelessWidget {
  const CreditItApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => UserProvider()),
        ChangeNotifierProvider(create: (_) => ChatbotProvider()),
      ],
      child: MaterialApp(
        title: 'Credit-It',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        home: const HomeScreen(),
      ),
    );
  }
}
