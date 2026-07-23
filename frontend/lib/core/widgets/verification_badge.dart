import 'package:flutter/material.dart';

enum VerificationType {
  verified,
  officialSource,
  publicRecord,
  aiSummary,
  sampleData,
  unavailable,
}

class VerificationBadge extends StatelessWidget {
  final VerificationType type;
  final String? customLabel;

  const VerificationBadge({
    super.key,
    required this.type,
    this.customLabel,
  });

  @override
  Widget build(BuildContext context) {
    final config = _getBadgeConfig();
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: config.color.withValues(alpha: isDark ? 0.12 : 0.08),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: config.color.withValues(alpha: isDark ? 0.3 : 0.2),
          width: 1,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(config.icon, color: config.color, size: 12),
          const SizedBox(width: 5),
          Text(
            customLabel ?? config.label,
            style: TextStyle(
              color: config.color,
              fontSize: 11,
              fontWeight: FontWeight.w600,
              letterSpacing: -0.2,
            ),
          ),
        ],
      ),
    );
  }

  _BadgeConfig _getBadgeConfig() {
    switch (type) {
      case VerificationType.verified:
        return const _BadgeConfig(
          label: 'Verified',
          icon: Icons.check_circle,
          color: Color(0xFF10B981),
        );
      case VerificationType.officialSource:
        return const _BadgeConfig(
          label: 'Official Source',
          icon: Icons.verified,
          color: Color(0xFF2563EB),
        );
      case VerificationType.publicRecord:
        return const _BadgeConfig(
          label: 'Public Record',
          icon: Icons.description,
          color: Color(0xFF0D9488),
        );
      case VerificationType.aiSummary:
        return const _BadgeConfig(
          label: 'AI Summary',
          icon: Icons.psychology,
          color: Color(0xFF8B5CF6),
        );
      case VerificationType.sampleData:
        return const _BadgeConfig(
          label: 'Sample Data',
          icon: Icons.science,
          color: Color(0xFFF59E0B),
        );
      case VerificationType.unavailable:
        return const _BadgeConfig(
          label: 'Data Not Available',
          icon: Icons.warning_amber_rounded,
          color: Color(0xFF6B7280),
        );
    }
  }
}

class _BadgeConfig {
  final String label;
  final IconData icon;
  final Color color;

  const _BadgeConfig({
    required this.label,
    required this.icon,
    required this.color,
  });
}
