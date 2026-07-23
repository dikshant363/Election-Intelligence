import 'package:election_intelligence_frontend/features/control_center/presentation/providers/control_center_providers.dart';
import 'package:election_intelligence_frontend/features/control_center/presentation/screens/control_center_shell_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

void main() {
  group('Control Center UI Tests', () {
    testWidgets('ControlCenterShellScreen renders correctly with navigation sidebar', (tester) async {
      // Set desktop viewport size for Control Center testing
      tester.view.physicalSize = const Size(1280, 800);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);

      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: ControlCenterShellScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // Verify header and branding
      expect(find.text('Election Intelligence'), findsOneWidget);
      expect(find.text('Control Center v1.0.0'), findsOneWidget);

      // Verify side navigation menu items
      expect(find.text('Enterprise Control Center'), findsNWidgets(2));
      expect(find.text('Executive Command Center'), findsOneWidget);
      expect(find.text('Operations Console'), findsOneWidget);
      expect(find.text('Public Portal'), findsOneWidget);
    });

    test('ControlInterfaceNotifier switches active interface', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      expect(
        container.read(controlInterfaceProvider),
        ControlInterface.enterpriseControlCenter,
      );

      container.read(controlInterfaceProvider.notifier).selectInterface(ControlInterface.executiveCommandCenter);

      expect(
        container.read(controlInterfaceProvider),
        ControlInterface.executiveCommandCenter,
      );
    });

    test('FeatureFlagsNotifier toggles flag state', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      final initialFlags = container.read(featureFlagsProvider);
      final ragFlag = initialFlags.firstWhere((f) => f.name == 'enable_rag');
      expect(ragFlag.enabled, isTrue);

      container.read(featureFlagsProvider.notifier).toggleFlag('enable_rag');

      final updatedFlags = container.read(featureFlagsProvider);
      final updatedRagFlag = updatedFlags.firstWhere((f) => f.name == 'enable_rag');
      expect(updatedRagFlag.enabled, isFalse);
    });
  });
}
