import 'package:election_intelligence_frontend/routing/app_router.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

void main() {
  group('AppRouter Tests', () {
    testWidgets('Router navigates to SplashScreen on initial route',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp.router(
            routerConfig: AppRouter.router,
          ),
        ),
      );
      await tester.pump();

      expect(find.text('Election Intelligence Platform'), findsOneWidget);
    });

    testWidgets('Router can navigate to HomeScreen / Citizen Portal',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp.router(
            routerConfig: AppRouter.router,
          ),
        ),
      );
      await tester.pump();

      AppRouter.router.go('/portal');
      await tester.pumpAndSettle();

      expect(find.text('Explore Indian Election & Candidate Affidavits'), findsOneWidget);
    });
  });
}
