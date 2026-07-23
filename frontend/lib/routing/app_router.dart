import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../core/widgets/verification_badge.dart';
import '../features/citizen/presentation/screens/candidate_comparison_screen.dart';
import '../features/citizen/presentation/screens/citizen_portal_screen.dart';
import '../features/control_center/presentation/screens/control_center_shell_screen.dart';
import '../features/splash/presentation/splash_screen.dart';

Widget _buildPlaceholderModule(String title, String subtitle, IconData icon) {
  return Scaffold(
    appBar: AppBar(
      title: Text(title),
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
      child: Card(
        margin: const EdgeInsets.all(24.0),
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 64, color: Colors.indigo),
              const SizedBox(height: 16),
              Text(
                title,
                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Text(
                subtitle,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.grey),
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
        builder: (context, state) => _buildPlaceholderModule(
          'Political Party Intelligence',
          'Explore party manifestos, seat shares, leadership timelines, and alliances.',
          Icons.flag,
        ),
      ),
      GoRoute(
        path: '/constituencies',
        builder: (context, state) => _buildPlaceholderModule(
          'Constituency Intelligence',
          'Explore electoral demographics, voter literacy, turnouts, and past margins.',
          Icons.location_city,
        ),
      ),
      GoRoute(
        path: '/elections',
        builder: (context, state) => _buildPlaceholderModule(
          'Election Intelligence',
          'Explore Lok Sabha, Vidhan Sabha, Municipal, and Panchayat election history.',
          Icons.how_to_vote,
        ),
      ),
      GoRoute(
        path: '/compare',
        builder: (context, state) => const CandidateComparisonScreen(),
      ),
      GoRoute(
        path: '/timeline',
        builder: (context, state) => _buildPlaceholderModule(
          'Election Timeline',
          'Chronological schedule of nominations, polling phases, and result declarations.',
          Icons.timeline,
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
        builder: (context, state) => _buildPlaceholderModule(
          'News & Public Records',
          'Verified news timeline and official Election Commission announcements.',
          Icons.newspaper,
        ),
      ),
      GoRoute(
        path: '/documents',
        builder: (context, state) => _buildPlaceholderModule(
          'Document Archive',
          'Verified Form 26 affidavit disclosures, gazette notifications, and PDFs.',
          Icons.description,
        ),
      ),
      GoRoute(
        path: '/maps',
        builder: (context, state) => _buildPlaceholderModule(
          'Spatial Maps',
          'Geospatial constituency boundaries and polling booth mapping.',
          Icons.map,
        ),
      ),
      GoRoute(
        path: '/statistics',
        builder: (context, state) => _buildPlaceholderModule(
          'Electoral Statistics',
          'Voter turnout, gender ratios, age distribution, and historical vote shares.',
          Icons.bar_chart,
        ),
      ),
      GoRoute(
        path: '/analytics',
        builder: (context, state) => _buildPlaceholderModule(
          'Visual Analytics',
          'Interactive charts and non-partisan electoral data insights.',
          Icons.analytics,
        ),
      ),
      GoRoute(
        path: '/saved',
        builder: (context, state) => _buildPlaceholderModule(
          'Saved Research',
          'Bookmarked candidate affidavits, constituency reports, and AI answers.',
          Icons.bookmark,
        ),
      ),
      GoRoute(
        path: '/profile',
        builder: (context, state) => _buildPlaceholderModule(
          'Citizen Profile',
          'Manage saved research, preferred constituency, and accessibility settings.',
          Icons.person,
        ),
      ),
      GoRoute(
        path: '/settings',
        builder: (context, state) => _buildPlaceholderModule(
          'Platform Settings',
          'Theme preferences, data transparency disclosures, and AI model settings.',
          Icons.settings,
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
