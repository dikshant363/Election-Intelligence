# Frontend Core Framework Guide

## Overview
The Election Intelligence Platform frontend is built with Flutter (SDK 3.16+ / Dart 3.2+) following clean feature-based architecture and modern reactive state management using **Riverpod** (`hooks_riverpod`).

## Key Principles

### 1. State Management & Dependency Injection
- **Riverpod (`hooks_riverpod`)** is the sole and single source of truth for both state management and dependency injection across the application.
- `GetIt` has been completely removed to maintain architectural consistency and single source of truth.

### 2. Application Bootstrap (`lib/main.dart`)
- Clean, minimal bootstrap script (30-50 lines).
- Initializes bindings with `WidgetsFlutterBinding.ensureInitialized()`.
- Registers global framework error handling (`FlutterError.onError`) and asynchronous platform error handling (`PlatformDispatcher.instance.onError`).
- Wraps the root `MyApp` inside `ProviderScope`.
- Only a single application bootstrap (`ProviderScope` -> `MyApp`) exists.

### 3. Declarative Routing (`lib/routing/app_router.dart`)
- Declarative route management using `GoRouter`.
- Pre-configured routes:
  - `/` -> `SplashScreen`
  - `/splash` -> `SplashScreen`
  - `/home` -> `HomeScreen`

### 4. Structured Logging (`lib/core/logging/logger.dart`)
- Centralized `Logger` utility replacing raw `debugPrint` statements.
- Direct error logging via `Logger.logError(...)` and structured level methods (`debug`, `info`, `error`).

### 5. Unified Design System & Theming (`lib/core/theme/app_theme.dart`)
- Material 3 design system.
- Standardized light theme (`AppTheme.light()`) and dark theme (`AppTheme.dark()`).
- Theme configuration dynamically supported in `MaterialApp.router`.

## Development Commands
```bash
# Analyze static code quality
flutter analyze

# Format code
dart format --set-exit-if-changed .

# Run test suite
flutter test
```
