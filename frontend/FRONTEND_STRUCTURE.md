# Frontend Structure & Architecture

## Directory Layout

```
frontend/
├── lib/
│   ├── main.dart                      # Clean application bootstrap entrypoint
│   ├── core/                          # Core system utilities & configurations
│   │   ├── logging/
│   │   │   └── logger.dart            # Centralized logging engine (Logger.logError)
│   │   └── theme/
│   │       └── app_theme.dart         # Material 3 light and dark theme definitions
│   ├── routing/
│   │   └── app_router.dart            # GoRouter route definitions and navigation
│   └── features/                      # Feature-driven module architecture
│       ├── home/
│       │   └── presentation/
│       │       └── home_screen.dart   # Home screen view component
│       └── splash/
│           └── presentation/
│               └── splash_screen.dart # Splash screen view component
├── test/                              # Comprehensive unit and widget tests
│   ├── app_test.dart                  # MyApp & ProviderScope initialization test
│   ├── logging/
│   │   └── logger_test.dart           # Logger module unit tests
│   ├── routing/
│   │   └── app_router_test.dart       # Routing and navigation widget tests
│   └── theme/
│       └── app_theme_test.dart        # AppTheme configuration unit tests
├── pubspec.yaml                       # Dependencies (Riverpod, GoRouter, Hooks)
├── FRONTEND_GUIDE.md                  # Development guide & architecture principles
├── FRONTEND_STRUCTURE.md              # Project structure documentation
└── FRONTEND_VALIDATION.md             # Verification & test execution report
```

## Architectural Conventions
1. **Feature-First Architecture**: Each domain capability is grouped inside `lib/features/<feature_name>/` containing `presentation/`, `domain/`, and `data/` sub-layers as expanded in future milestones.
2. **Core Layer**: Shared cross-cutting concerns (theming, logging, utilities) reside in `lib/core/`.
3. **No GetIt Service Locator**: Dependencies are injected exclusively via Riverpod providers.
