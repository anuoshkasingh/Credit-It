import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/chatbot_provider.dart';
import '../providers/user_provider.dart';
import '../screens/api_settings_screen.dart';
import '../theme/app_theme.dart';

class FloatingChatbotWidget extends StatefulWidget {
  final Widget child;

  const FloatingChatbotWidget({
    super.key,
    required this.child,
  });

  @override
  State<FloatingChatbotWidget> createState() => _FloatingChatbotWidgetState();
}

class _FloatingChatbotWidgetState extends State<FloatingChatbotWidget> {
  final TextEditingController _inputController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  @override
  void dispose() {
    _inputController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final chatbotProvider = Provider.of<ChatbotProvider>(context);
    final userProvider = Provider.of<UserProvider>(context);

    final bottomInset = MediaQuery.of(context).viewInsets.bottom;

    if (chatbotProvider.messages.isNotEmpty) {
      _scrollToBottom();
    }

    return Stack(
      children: [
        // Underneath Page Content
        widget.child,

        // Floating Action Button (Bottom-Right) when panel is closed
        if (!chatbotProvider.isOpen)
          Positioned(
            right: 16,
            bottom: 20,
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: () {
                  chatbotProvider.openPanel();
                },
                borderRadius: BorderRadius.circular(30),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [AppTheme.primaryBlue, Color(0xFF0052CC)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(30),
                    boxShadow: [
                      BoxShadow(
                        color: AppTheme.primaryBlue.withOpacity(0.4),
                        blurRadius: 14,
                        offset: const Offset(0, 6),
                      )
                    ],
                  ),
                  child: const Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.auto_awesome, color: Colors.amber, size: 20),
                      SizedBox(width: 8),
                      Text(
                        'Credit It Assistant',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 13,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),

        // Floating Chat Panel Overlay (over current screen)
        if (chatbotProvider.isOpen) ...[
          // Backdrop to close panel when tapping anywhere outside
          Positioned.fill(
            child: GestureDetector(
              onTap: () {
                FocusScope.of(context).unfocus();
                chatbotProvider.closePanel();
              },
              behavior: HitTestBehavior.opaque,
              child: Container(
                color: Colors.black.withOpacity(0.2),
              ),
            ),
          ),

          // Floating Panel with Dynamic Keyboard Avoidance
          AnimatedPositioned(
            duration: const Duration(milliseconds: 180),
            curve: Curves.easeOutCubic,
            right: 12,
            left: 12,
            bottom: 16 + bottomInset,
            top: bottomInset > 0 ? 50 : MediaQuery.of(context).size.height * 0.22,
            child: Material(
              elevation: 16,
              borderRadius: BorderRadius.circular(20),
              child: Container(
                decoration: BoxDecoration(
                  color: const Color(0xFFF9FAFC),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppTheme.borderLight, width: 1.2),
                ),
                child: Column(
                  children: [
                    // Header Bar
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      decoration: const BoxDecoration(
                        color: AppTheme.primaryBlue,
                        borderRadius: BorderRadius.vertical(top: Radius.circular(18)),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.auto_awesome, color: Colors.amber, size: 20),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Credit It Assistant',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 15,
                                  ),
                                ),
                                if (chatbotProvider.activeCardRec != null)
                                  Text(
                                    '📍 Context: ${chatbotProvider.activeCardRec!.card.cardName}',
                                    style: const TextStyle(
                                      color: Colors.amber,
                                      fontSize: 10.5,
                                      fontWeight: FontWeight.w600,
                                    ),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  )
                                else
                                  const Text(
                                    'Personalized AI Financial Advisor',
                                    style: TextStyle(color: Colors.white70, fontSize: 10.5),
                                  ),
                              ],
                            ),
                          ),
                          // Settings Button (API Settings)
                          IconButton(
                            icon: const Icon(Icons.settings_outlined, color: Colors.white, size: 20),
                            tooltip: 'API Settings',
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (context) => const ApiSettingsScreen()),
                              );
                            },
                          ),
                          // Close Button
                          IconButton(
                            icon: const Icon(Icons.close, color: Colors.white, size: 20),
                            onPressed: () => chatbotProvider.closePanel(),
                          ),
                        ],
                      ),
                    ),

                    // Quick Suggestion Chips
                    Container(
                      height: 40,
                      padding: const EdgeInsets.symmetric(horizontal: 10),
                      color: Colors.blue.shade50.withOpacity(0.5),
                      child: ListView(
                        scrollDirection: Axis.horizontal,
                        children: [
                          _buildSuggestionChip(
                            context,
                            chatbotProvider.activeCardRec != null
                                ? 'Why was this card recommended?'
                                : 'Why were these cards recommended?',
                            chatbotProvider,
                            userProvider,
                          ),
                          _buildSuggestionChip(
                            context,
                            'Compare Axis Atlas and Infinia',
                            chatbotProvider,
                            userProvider,
                          ),
                          _buildSuggestionChip(
                            context,
                            'What does lounge access mean?',
                            chatbotProvider,
                            userProvider,
                          ),
                          _buildSuggestionChip(
                            context,
                            'What does 5X rewards mean?',
                            chatbotProvider,
                            userProvider,
                          ),
                        ],
                      ),
                    ),

                    // Message List
                    Expanded(
                      child: ListView.builder(
                        controller: _scrollController,
                        padding: const EdgeInsets.all(12),
                        itemCount: chatbotProvider.messages.length,
                        itemBuilder: (context, index) {
                          final msg = chatbotProvider.messages[index];
                          return _buildMessageBubble(context, msg);
                        },
                      ),
                    ),

                    // Typing Loading Indicator
                    if (chatbotProvider.isLoading)
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                        child: Row(
                          children: [
                            const SizedBox(
                              width: 14,
                              height: 14,
                              child: CircularProgressIndicator(strokeWidth: 2, color: AppTheme.primaryBlue),
                            ),
                            const SizedBox(width: 8),
                            Text(
                              'Credit It Assistant is thinking...',
                              style: TextStyle(fontSize: 11.5, color: Colors.grey.shade600, fontStyle: FontStyle.italic),
                            ),
                          ],
                        ),
                      ),

                    // Bottom Input Row
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: const BorderRadius.vertical(bottom: Radius.circular(18)),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.05),
                            blurRadius: 4,
                            offset: const Offset(0, -2),
                          ),
                        ],
                      ),
                      child: Row(
                        children: [
                          Expanded(
                            child: TextField(
                              controller: _inputController,
                              textInputAction: TextInputAction.send,
                              onSubmitted: (val) {
                                if (val.trim().isNotEmpty) {
                                  chatbotProvider.sendMessage(val, userProvider);
                                  _inputController.clear();
                                }
                              },
                              decoration: const InputDecoration(
                                hintText: 'Ask Credit It Assistant...',
                                border: InputBorder.none,
                                hintStyle: TextStyle(fontSize: 13, color: Colors.grey),
                                contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                              ),
                              style: const TextStyle(fontSize: 13.5),
                            ),
                          ),
                          const SizedBox(width: 6),
                          Material(
                            color: AppTheme.primaryBlue,
                            borderRadius: BorderRadius.circular(20),
                            child: InkWell(
                              borderRadius: BorderRadius.circular(20),
                              onTap: () {
                                final text = _inputController.text.trim();
                                if (text.isNotEmpty) {
                                  chatbotProvider.sendMessage(text, userProvider);
                                  _inputController.clear();
                                }
                              },
                              child: const Padding(
                                padding: EdgeInsets.all(10),
                                child: Icon(Icons.send, color: Colors.white, size: 18),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildSuggestionChip(
    BuildContext context,
    String label,
    ChatbotProvider chatbotProvider,
    UserProvider userProvider,
  ) {
    return Padding(
      padding: const EdgeInsets.only(right: 6, top: 6, bottom: 6),
      child: ActionChip(
        label: Text(label, style: const TextStyle(fontSize: 10.5, color: AppTheme.primaryBlue, fontWeight: FontWeight.w600)),
        backgroundColor: Colors.white,
        side: const BorderSide(color: AppTheme.primaryBlue, width: 0.8),
        padding: const EdgeInsets.symmetric(horizontal: 6),
        materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
        onPressed: () {
          chatbotProvider.sendMessage(label, userProvider);
        },
      ),
    );
  }

  Widget _buildMessageBubble(BuildContext context, dynamic msg) {
    final isUser = msg.isUser;
    final isError = msg.isError;

    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.75,
        ),
        decoration: BoxDecoration(
          color: isUser
              ? AppTheme.primaryBlue
              : (isError ? Colors.red.shade50 : Colors.white),
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(14),
            topRight: const Radius.circular(14),
            bottomLeft: Radius.circular(isUser ? 14 : 2),
            bottomRight: Radius.circular(isUser ? 2 : 14),
          ),
          border: Border.all(
            color: isUser
                ? AppTheme.primaryBlue
                : (isError ? Colors.red.shade200 : AppTheme.borderLight),
            width: 1,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (msg.contextLabel != null && isUser)
              Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Text(
                  '📍 Context: ${msg.contextLabel}',
                  style: const TextStyle(fontSize: 9.5, color: Colors.amber, fontWeight: FontWeight.bold),
                ),
              ),
            Text(
              msg.text,
              style: TextStyle(
                fontSize: 13,
                height: 1.35,
                color: isUser
                    ? Colors.white
                    : (isError ? Colors.red.shade900 : AppTheme.textDark),
              ),
            ),
            if (isError) ...[
              const SizedBox(height: 6),
              GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const ApiSettingsScreen()),
                  );
                },
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.settings, size: 12, color: Colors.red.shade800),
                    const SizedBox(width: 4),
                    Text(
                      'Open API Settings ->',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: Colors.red.shade800,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
