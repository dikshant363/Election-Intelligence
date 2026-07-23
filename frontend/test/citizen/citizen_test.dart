import 'package:election_intelligence_frontend/core/widgets/verification_badge.dart';
import 'package:election_intelligence_frontend/features/citizen/presentation/screens/citizen_portal_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

void main() {
  group('VerificationBadge Widget Tests', () {
    testWidgets('Renders Official Source badge correctly', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: VerificationBadge(type: VerificationType.officialSource),
          ),
        ),
      );

      expect(find.text('Official Source'), findsOneWidget);
      expect(find.byIcon(Icons.verified), findsOneWidget);
    });

    testWidgets('Renders Verified badge correctly', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: VerificationBadge(type: VerificationType.verified),
          ),
        ),
      );

      expect(find.text('Verified'), findsOneWidget);
      expect(find.byIcon(Icons.check_circle), findsOneWidget);
    });
  });

  group('CitizenPortalScreen Widget Tests', () {
    testWidgets('Renders Citizen Portal with search and candidate profiles', (tester) async {
      tester.view.physicalSize = const Size(1280, 800);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);

      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: CitizenPortalScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      expect(find.text('Explore Indian Election & Candidate Affidavits'), findsOneWidget);
      expect(find.text('Narendra Modi'), findsOneWidget);
      expect(find.text('Rahul Gandhi'), findsOneWidget);
      expect(find.text('Akhilesh Yadav'), findsOneWidget);
    });
  });
}
