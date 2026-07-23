import 'package:election_intelligence_frontend/main.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

void main() {
  testWidgets('MyApp renders MaterialApp.router with ProviderScope',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: MyApp(),
      ),
    );
    await tester.pump();

    expect(find.text('Election Intelligence Platform'), findsOneWidget);
  });
}
