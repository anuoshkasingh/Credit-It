import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/user_provider.dart';
import '../theme/app_theme.dart';

class CategoryFilterTabs extends StatelessWidget {
  const CategoryFilterTabs({super.key});

  final List<String> categories = const ['All', 'Shopping', 'Travel', 'Utilities', 'Food'];

  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);
    final selectedCategory = userProvider.selectedCategory;

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: categories.map((cat) {
          final isSelected = selectedCategory == cat;
          return Padding(
            padding: const EdgeInsets.only(right: 8),
            child: ChoiceChip(
              label: Text(
                cat,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  color: isSelected ? Colors.white : AppTheme.primaryBlue,
                ),
              ),
              selected: isSelected,
              selectedColor: AppTheme.primaryBlue,
              backgroundColor: Colors.white,
              elevation: isSelected ? 2 : 0,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
                side: BorderSide(
                  color: isSelected ? AppTheme.primaryBlue : AppTheme.borderLight,
                ),
              ),
              onSelected: (_) {
                userProvider.setCategoryFilter(cat);
              },
            ),
          );
        }).toList(),
      ),
    );
  }
}
