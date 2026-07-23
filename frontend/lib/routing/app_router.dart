import 'package:go_router/go_router.dart';

import '../features/citizen/presentation/screens/citizen_portal_screen.dart';
import '../features/control_center/presentation/screens/control_center_shell_screen.dart';
import '../features/home/presentation/home_screen.dart';
import '../features/splash/presentation/splash_screen.dart';

class AppRouter {
  static final router = GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: '/splash',
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: '/portal',
        builder: (context, state) => const CitizenPortalScreen(),
      ),
      GoRoute(
        path: '/home',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: '/control-center',
        builder: (context, state) => const ControlCenterShellScreen(),
      ),
      GoRoute(
        path: '/admin',
        builder: (context, state) => const ControlCenterShellScreen(),
      ),
      GoRoute(
        path: '/ops',
        builder: (context, state) => const ControlCenterShellScreen(),
      ),
      GoRoute(
        path: '/executive',
        builder: (context, state) => const ControlCenterShellScreen(),
      ),
    ],
  );
}
