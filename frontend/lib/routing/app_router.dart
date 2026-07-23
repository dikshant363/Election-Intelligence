import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../core/widgets/verification_badge.dart';
import '../features/citizen/presentation/screens/candidate_comparison_screen.dart';
import '../features/citizen/presentation/screens/citizen_portal_screen.dart';
import '../features/control_center/presentation/screens/control_center_shell_screen.dart';
import '../features/splash/presentation/splash_screen.dart';

Widget _buildModuleView(String title, String subtitle, IconData icon) {
  return Scaffold(
    appBar: AppBar(
      title: Text(
        title,
        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w700, letterSpacing: -0.5),
      ),
      actions: const [
        Padding(
          padding: EdgeInsets.symmetric(horizontal: 16.0),
          child: Center(
            child: VerificationBadge(
              type: VerificationType.publicRecord,
              customLabel: 'Verified Record',
            ),
          ),
        ),
      ],
    ),
    body: Center(
      child: Container(
        constraints: const BoxConstraints(maxWidth: 600),
        margin: const EdgeInsets.all(24.0),
        padding: const EdgeInsets.all(32.0),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: const Color(0xFFE5E7EB), width: 1),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 48, color: const Color(0xFF2563EB)),
            const SizedBox(height: 20),
            Text(
              title,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w700, letterSpacing: -0.5),
            ),
            const SizedBox(height: 8),
            Text(
              subtitle,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 14, color: Color(0xFF6B7280), height: 1.4),
            ),
            const SizedBox(height: 24),
            const VerificationBadge(
              type: VerificationType.officialSource,
              customLabel: 'ECI Official Data Source',
            ),
          ],
        ),
      ),
    ),
  );
}

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
        builder: (context, state) => const CitizenPortalScreen(),
      ),
      GoRoute(
        path: '/candidates',
        builder: (context, state) => const CitizenPortalScreen(),
      ),
      GoRoute(
        path: '/parties',
        builder: (context, state) => _buildModuleView(
          'Political Party Intelligence',
          'Explore party manifestos, seat shares, leadership timelines, and alliances.',
          Icons.flag_outlined,
        ),
      ),
      GoRoute(
        path: '/constituencies',
        builder: (context, state) => _buildModuleView(
          'Constituency Intelligence',
          'Explore electoral demographics, voter literacy, turnouts, and past margins.',
          Icons.location_city_outlined,
        ),
      ),
      GoRoute(
        path: '/elections',
        builder: (context, state) => _buildModuleView(
          'Election Intelligence',
          'Explore Lok Sabha, Vidhan Sabha, Municipal, and Panchayat election history.',
          Icons.how_to_vote_outlined,
        ),
      ),
      GoRoute(
        path: '/compare',
        builder: (context, state) => const CandidateComparisonScreen(),
      ),
      GoRoute(
        path: '/timeline',
        builder: (context, state) => _buildModuleView(
          'Election Timeline',
          'Chronological schedule of nominations, polling phases, and result declarations.',
          Icons.timeline_outlined,
        ),
      ),
      GoRoute(
        path: '/ai-assistant',
        builder: (context, state) => const CitizenPortalScreen(),
      ),
      GoRoute(
        path: '/search',
        builder: (context, state) => const CitizenPortalScreen(),
      ),
      GoRoute(
        path: '/news',
        builder: (context, state) => _buildModuleView(
          'News & Public Records',
          'Verified news timeline and official Election Commission announcements.',
          Icons.newspaper_outlined,
        ),
      ),
      GoRoute(
        path: '/documents',
        builder: (context, state) => _buildModuleView(
          'Document Archive',
          'Verified Form 26 affidavit disclosures, gazette notifications, and PDFs.',
          Icons.description_outlined,
        ),
      ),
      GoRoute(
        path: '/maps',
        builder: (context, state) => _buildModuleView(
          'Spatial Maps',
          'Geospatial constituency boundaries and polling booth mapping.',
          Icons.map_outlined,
        ),
      ),
      GoRoute(
        path: '/statistics',
        builder: (context, state) => _buildModuleView(
          'Electoral Statistics',
          'Voter turnout, gender ratios, age distribution, and historical vote shares.',
          Icons.bar_chart_outlined,
        ),
      ),
      GoRoute(
        path: '/analytics',
        builder: (context, state) => _buildModuleView(
          'Visual Analytics',
          'Interactive charts and non-partisan electoral data insights.',
          Icons.analytics_outlined,
        ),
      ),
      GoRoute(
        path: '/saved',
        builder: (context, state) => _buildModuleView(
          'Saved Research',
          'Bookmarked candidate affidavits, constituency reports, and AI answers.',
          Icons.bookmark_outline,
        ),
      ),
      GoRoute(
        path: '/profile',
        builder: (context, state) => _buildModuleView(
          'Citizen Profile',
          'Manage saved research, preferred constituency, and accessibility settings.',
          Icons.person_outline,
        ),
      ),
      GoRoute(
        path: '/settings',
        builder: (context, state) => _buildModuleView(
          'Platform Settings',
          'Theme preferences, data transparency disclosures, and AI model settings.',
          Icons.settings_outlined,
        ),
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
