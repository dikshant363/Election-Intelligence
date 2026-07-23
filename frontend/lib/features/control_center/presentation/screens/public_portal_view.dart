import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import '../../../citizen/presentation/screens/citizen_portal_screen.dart';

class PublicPortalView extends ConsumerWidget {
  const PublicPortalView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return const CitizenPortalScreen();
  }
}
