// This is a basic Flutter widget test for LegalEasier app.

import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:legaleasier/main.dart';

void main() {
  testWidgets('LegalEasier app smoke test', (WidgetTester tester) async {
    // Build our app
    await tester.pumpWidget(
      const ProviderScope(
        child: LegalEasierApp(),
      ),
    );
    await tester.pumpAndSettle();

    // Verify app launched without errors
    expect(find.byType(LegalEasierApp), findsOneWidget);
  });
}
