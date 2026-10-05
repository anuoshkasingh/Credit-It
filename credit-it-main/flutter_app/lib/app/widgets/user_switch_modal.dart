import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/chatbot_provider.dart';
import '../providers/user_provider.dart';
import '../screens/api_settings_screen.dart';
import '../theme/app_theme.dart';

class UserSwitchModal extends StatelessWidget {
  const UserSwitchModal({super.key});

  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);
    final currentUser = userProvider.currentUser;
    final users = userProvider.users;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Select User Profile',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.primaryBlue,
                ),
              ),
              IconButton(
                icon: const Icon(Icons.close),
                onPressed: () => Navigator.pop(context),
              ),
            ],
          ),
          const SizedBox(height: 12),
          ...users.map((user) {
            final isSelected = currentUser?.userId == user.userId;

            return Container(
              margin: const EdgeInsets.only(bottom: 12),
              decoration: BoxDecoration(
                color: isSelected ? AppTheme.accentBlue.withOpacity(0.08) : Colors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: isSelected ? AppTheme.accentBlue : AppTheme.borderLight,
                  width: isSelected ? 2 : 1,
                ),
              ),
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: isSelected ? AppTheme.primaryBlue : Colors.grey.shade200,
                  foregroundColor: isSelected ? Colors.white : Colors.black87,
                  child: Text(
                    user.initials,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
                title: Text(
                  user.name,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: isSelected ? AppTheme.primaryBlue : AppTheme.textDark,
                  ),
                ),
                trailing: isSelected
                    ? const Icon(Icons.check_circle, color: AppTheme.accentBlue)
                    : const Icon(Icons.radio_button_unchecked, color: Colors.grey),
                onTap: () {
                  if (currentUser?.userId != user.userId) {
                    userProvider.switchUser(user);
                    Provider.of<ChatbotProvider>(context, listen: false).clearChat();
                  }
                  Navigator.pop(context);
                },
              ),
            );
          }),
          const Divider(height: 24),
          ListTile(
            leading: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppTheme.primaryBlue.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.settings, color: AppTheme.primaryBlue, size: 20),
            ),
            title: const Text(
              'API Settings',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: AppTheme.primaryBlue),
            ),
            subtitle: const Text('Configure Gemini API key for Credit It Assistant', style: TextStyle(fontSize: 11)),
            trailing: const Icon(Icons.chevron_right, color: AppTheme.primaryBlue),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ApiSettingsScreen()),
              );
            },
          ),
          const SizedBox(height: 12),
        ],
      ),
    );
  }
}
