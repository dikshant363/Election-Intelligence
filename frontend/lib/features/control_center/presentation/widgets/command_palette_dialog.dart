import 'package:flutter/material.dart';

class CommandPaletteDialog extends StatefulWidget {
  const CommandPaletteDialog({super.key});

  @override
  State<CommandPaletteDialog> createState() => _CommandPaletteDialogState();
}

class _CommandPaletteDialogState extends State<CommandPaletteDialog> {
  final TextEditingController _searchController = TextEditingController();
  String _filter = '';

  final List<Map<String, String>> _commands = const [
    {'title': 'View System Telemetry & Health', 'category': 'Enterprise Control', 'icon': 'monitor_heart'},
    {'title': 'Manage Feature Flags', 'category': 'Enterprise Control', 'icon': 'flag'},
    {'title': 'AI Model Routing & Prompts', 'category': 'AI Control', 'icon': 'psychology'},
    {'title': 'Security Audit Logs', 'category': 'Security Governance', 'icon': 'shield'},
    {'title': 'User Accounts & Roles (RBAC)', 'category': 'Security Governance', 'icon': 'people'},
    {'title': 'Flush Cache (Redis & Memory)', 'category': 'Operations', 'icon': 'cleaning_services'},
    {'title': 'Reindex Search Engine (SAL)', 'category': 'Operations', 'icon': 'search'},
    {'title': 'Ingest Election Data (ETL)', 'category': 'Operations Console', 'icon': 'upload_file'},
    {'title': 'Executive KPIs & Turnout Analytics', 'category': 'Executive Command', 'icon': 'bar_chart'},
    {'title': 'Public Portal Information', 'category': 'Public Portal', 'icon': 'public'},
  ];

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final filtered = _commands.where((cmd) {
      final query = _filter.toLowerCase();
      return cmd['title']!.toLowerCase().contains(query) ||
          cmd['category']!.toLowerCase().contains(query);
    }).toList();

    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        width: 600,
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: _searchController,
              autofocus: true,
              decoration: InputDecoration(
                hintText: 'Type a command or search modules... (e.g. AI, Users, Cache)',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () => Navigator.of(context).pop(),
                ),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              onChanged: (val) => setState(() => _filter = val),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 320,
              child: filtered.isEmpty
                  ? Center(
                      child: Text(
                        'No matching commands found',
                        style: theme.textTheme.bodyLarge?.copyWith(
                          color: theme.colorScheme.onSurfaceVariant,
                        ),
                      ),
                    )
                  : ListView.builder(
                      itemCount: filtered.length,
                      itemBuilder: (context, index) {
                        final cmd = filtered[index];
                        return ListTile(
                          leading: Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: theme.colorScheme.primaryContainer,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Icon(
                              _getIconData(cmd['icon']!),
                              color: theme.colorScheme.onPrimaryContainer,
                              size: 20,
                            ),
                          ),
                          title: Text(cmd['title']!),
                          subtitle: Text(cmd['category']!),
                          trailing: const Icon(Icons.arrow_forward_ios, size: 14),
                          onTap: () {
                            Navigator.of(context).pop(cmd['title']);
                          },
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }

  IconData _getIconData(String iconName) {
    switch (iconName) {
      case 'monitor_heart':
        return Icons.monitor_heart;
      case 'flag':
        return Icons.flag;
      case 'psychology':
        return Icons.psychology;
      case 'shield':
        return Icons.shield;
      case 'people':
        return Icons.people;
      case 'cleaning_services':
        return Icons.cleaning_services;
      case 'search':
        return Icons.search;
      case 'upload_file':
        return Icons.upload_file;
      case 'bar_chart':
        return Icons.bar_chart;
      case 'public':
        return Icons.public;
      default:
        return Icons.bolt;
    }
  }
}
