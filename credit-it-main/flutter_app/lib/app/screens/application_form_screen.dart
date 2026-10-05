import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/recommendation.dart';
import '../providers/user_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/floating_chatbot_widget.dart';
import '../services/api_service.dart';

class ApplicationFormScreen extends StatefulWidget {
  final CardRecommendation recommendation;

  const ApplicationFormScreen({
    super.key,
    required this.recommendation,
  });

  @override
  State<ApplicationFormScreen> createState() => _ApplicationFormScreenState();
}

class _ApplicationFormScreenState extends State<ApplicationFormScreen> {
  final int _currentStep = 1;
  late TextEditingController _panController;
  late TextEditingController _dobController;
  late TextEditingController _nameController;
  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    final user = Provider.of<UserProvider>(context, listen: false).currentUser;
    _panController = TextEditingController(text: user?.pan ?? 'ABCDE1234F');
    _dobController = TextEditingController(text: user?.dob ?? '15/08/1995');
    _nameController = TextEditingController(text: user?.name ?? 'Rohan Sharma');
  }

  @override
  void dispose() {
    _panController.dispose();
    _dobController.dispose();
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _handleVerifyAndSubmit() async {
    setState(() {
      _isSubmitting = true;
    });

    final user = Provider.of<UserProvider>(context, listen: false).currentUser;
    final formData = {
      "user_id": user?.userId ?? "001",
      "card_id": widget.recommendation.card.cardId,
      "pan": _panController.text,
      "dob": _dobController.text,
      "full_name": _nameController.text,
    };

    final success = await ApiService.submitApplication(formData);

    setState(() {
      _isSubmitting = false;
    });

    if (success && mounted) {
      _showSuccessDialog();
    }
  }

  void _showSuccessDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const CircleAvatar(
              radius: 36,
              backgroundColor: AppTheme.greenPositive,
              child: Icon(Icons.check, size: 40, color: Colors.white),
            ),
            const SizedBox(height: 16),
            const Text(
              'Application Submitted!',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: AppTheme.primaryBlue,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Your application for ${widget.recommendation.card.cardName} has been submitted to ${widget.recommendation.card.bankName}.',
              textAlign: TextAlign.center,
              style: const TextStyle(color: AppTheme.textSecondary, fontSize: 13),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: AppTheme.backgroundLight,
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Text(
                'Application ID: APP_CRIT_884920\nEst. Approval Time: < 2 Hours',
                textAlign: TextAlign.center,
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
              ),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pop(ctx); // Close dialog
                  Navigator.pop(context); // Close Application form screen
                  Navigator.pop(context); // Back to Home
                },
                child: const Text('Back to Home'),
              ),
            )
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return FloatingChatbotWidget(
      child: Scaffold(
        backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        foregroundColor: AppTheme.primaryBlue,
        elevation: 0,
        title: const Text(
          'Application Form',
          style: TextStyle(
            color: AppTheme.primaryBlue,
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.help_outline),
            onPressed: () {},
          )
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. Multi-step Progress Stepper (Light Theme)
            Container(
              padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 10),
              color: AppTheme.backgroundLight,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildStepCircle(1, 'PAN\nVerification', isActive: _currentStep >= 1),
                  _buildStepLine(_currentStep >= 2),
                  _buildStepCircle(2, 'Personal\nDetails', isActive: _currentStep >= 2),
                  _buildStepLine(_currentStep >= 3),
                  _buildStepCircle(3, 'Employment\nDetails', isActive: _currentStep >= 3),
                  _buildStepLine(_currentStep >= 4),
                  _buildStepCircle(4, 'Address\nDetails', isActive: _currentStep >= 4),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // 2. PAN Verification Form Content (Matching Screenshot Page 23)
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'PAN details',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.textDark,
                    ),
                  ),
                  const SizedBox(height: 10),

                  // PAN Input Box
                  TextField(
                    controller: _panController,
                    decoration: InputDecoration(
                      prefixIcon: Container(
                        margin: const EdgeInsets.all(10),
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.purple.shade100,
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: const Text(
                          'PAN',
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: Colors.purple,
                          ),
                        ),
                      ),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(color: AppTheme.borderLight),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(color: AppTheme.primaryBlue, width: 2),
                      ),
                    ),
                  ),

                  const SizedBox(height: 20),

                  const Text(
                    'Date of birth',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.textDark,
                    ),
                  ),
                  const SizedBox(height: 10),

                  // DOB Input Box
                  TextField(
                    controller: _dobController,
                    decoration: InputDecoration(
                      suffixIcon: const Icon(Icons.calendar_today_outlined, color: AppTheme.primaryBlue),
                      hintText: 'DD/MM/YYYY',
                      helperText: 'Please enter your date of birth as per PAN Card',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(color: AppTheme.borderLight),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(color: AppTheme.primaryBlue, width: 2),
                      ),
                    ),
                  ),

                  const SizedBox(height: 20),

                  const Text(
                    'Name as per PAN',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.textDark,
                    ),
                  ),
                  const SizedBox(height: 10),

                  // Name Input Box
                  TextField(
                    controller: _nameController,
                    decoration: InputDecoration(
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(color: AppTheme.borderLight),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(color: AppTheme.primaryBlue, width: 2),
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 30),

            // 3. Pre-filled Note Banner & Verify Button
            Container(
              color: Colors.white,
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.orange.shade50,
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: Colors.orange.shade200),
                    ),
                    child: const Row(
                      children: [
                        Icon(Icons.info_outline, color: Colors.orange, size: 18),
                        SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            'Note: Details previously provided to Credit-It are pre-filled in the application',
                            style: TextStyle(fontSize: 12, color: Colors.black87),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.primaryBlue,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      onPressed: _isSubmitting ? null : _handleVerifyAndSubmit,
                      child: _isSubmitting
                          ? const SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                            )
                          : const Text(
                              'Verify PAN & Submit Application',
                              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                            ),
                    ),
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    ),
    );
  }

  Widget _buildStepCircle(int step, String label, {required bool isActive}) {
    return Column(
      children: [
        CircleAvatar(
          radius: 14,
          backgroundColor: isActive ? AppTheme.greenPositive : Colors.grey.shade300,
          child: Text(
            '$step',
            style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 10,
            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
            color: isActive ? AppTheme.textDark : Colors.grey,
          ),
        )
      ],
    );
  }

  Widget _buildStepLine(bool isActive) {
    return Container(
      width: 24,
      height: 2,
      color: isActive ? AppTheme.greenPositive : Colors.grey.shade300,
    );
  }
}
