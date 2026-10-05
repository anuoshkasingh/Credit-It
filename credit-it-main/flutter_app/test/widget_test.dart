import 'package:flutter_test/flutter_test.dart';
import 'package:credit_it/main.dart';

void main() {
  testWidgets('Credit-It smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const CreditItApp());
    expect(find.text('Credit-'), findsOneWidget);
  });
}
