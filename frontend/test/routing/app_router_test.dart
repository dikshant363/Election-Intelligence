import 'package:election_intelligence_frontend/routing/app_router.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('AppRouter Tests', () {
    testWidgets('Router navigates to SplashScreen on initial route',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp.router(
          routerConfig: AppRouter.router,
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Election Intelligence Platform'), findsOneWidget);
    });

    testWidgets('Router can navigate to HomeScreen',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp.router(
          routerConfig: AppRouter.router,
        ),
      );
      await tester.pumpAndSettle();

      AppRouter.router.go('/home');
      await tester.pumpAndSettle();

      expect(find.text('Home Screen Placeholder'), findsOneWidget);
    });
  });
}
