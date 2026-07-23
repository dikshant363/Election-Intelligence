import 'package:election_intelligence_frontend/core/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('AppTheme Tests', () {
    test('light theme creates valid ThemeData with Material 3', () {
      final theme = AppTheme.light();
      expect(theme.useMaterial3, isTrue);
      expect(theme.brightness, equals(Brightness.light));
      expect(theme.scaffoldBackgroundColor, equals(const Color(0xFFF8F9FA)));
    });

    test('dark theme creates valid ThemeData with Material 3', () {
      final theme = AppTheme.dark();
      expect(theme.useMaterial3, isTrue);
      expect(theme.brightness, equals(Brightness.dark));
      expect(theme.scaffoldBackgroundColor, equals(const Color(0xFF121212)));
    });
  });
}
