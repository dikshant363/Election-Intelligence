import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import '../providers/control_center_providers.dart';
import '../widgets/command_palette_dialog.dart';
import '../widgets/control_center_sidebar.dart';
import 'enterprise_control_center_view.dart';
import 'executive_command_center_view.dart';
import 'operations_console_view.dart';
import 'public_portal_view.dart';

class ControlCenterShellScreen extends ConsumerWidget {
  const ControlCenterShellScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final currentInterface = ref.watch(controlInterfaceProvider);
    final theme = Theme.of(context);

    Widget activeView;
    switch (currentInterface) {
      case ControlInterface.enterpriseControlCenter:
        activeView = const EnterpriseControlCenterView();
        break;
      case ControlInterface.executiveCommandCenter:
        activeView = const ExecutiveCommandCenterView();
        break;
      case ControlInterface.operationsConsole:
        activeView = const OperationsConsoleView();
        break;
      case ControlInterface.publicPortal:
        activeView = const PublicPortalView();
        break;
    }

    return Scaffold(
      body: Row(
        children: [
          // Left Navigation Sidebar
          const ControlCenterSidebar(),

          // Main Workspace Body
          Expanded(
            child: Column(
              children: [
                // Top Header Bar
                Container(
                  height: 64,
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  decoration: BoxDecoration(
                    color: theme.colorScheme.surface,
                    border: Border(
                      bottom: BorderSide(
                        color: theme.colorScheme.outlineVariant.withValues(alpha: 0.5),
                        width: 1,
                      ),
                    ),
                  ),
                  child: SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: [
                        // Interface Breadcrumb / Title
                        Text(
                          _getInterfaceTitle(currentInterface),
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(width: 24),

                        // Command Palette Trigger (Cmd/Ctrl + K)
                        InkWell(
                          onTap: () {
                            showDialog<String>(
                              context: context,
                              builder: (context) => const CommandPaletteDialog(),
                            );
                          },
                          borderRadius: BorderRadius.circular(10),
                          child: Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 12,
                              vertical: 6,
                            ),
                            decoration: BoxDecoration(
                              color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(
                                color: theme.colorScheme.outlineVariant,
                              ),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  Icons.search,
                                  size: 16,
                                  color: theme.colorScheme.onSurfaceVariant,
                                ),
                                const SizedBox(width: 8),
                                Text(
                                  'Quick Search & Commands...',
                                  style: theme.textTheme.bodySmall?.copyWith(
                                    color: theme.colorScheme.onSurfaceVariant,
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 6,
                                    vertical: 2,
                                  ),
                                  decoration: BoxDecoration(
                                    color: theme.colorScheme.surface,
                                    borderRadius: BorderRadius.circular(4),
                                  ),
                                  child: Text(
                                    '⌘ K',
                                    style: theme.textTheme.labelSmall?.copyWith(
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(width: 16),

                        // System Status Badge
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 10,
                            vertical: 6,
                          ),
                          decoration: BoxDecoration(
                            color: Colors.green.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: const Row(
                            children: [
                              Icon(Icons.circle, color: Colors.green, size: 8),
                              SizedBox(width: 6),
                              Text(
                                'ALL SYSTEMS NORMAL',
                                style: TextStyle(
                                  color: Colors.green,
                                  fontSize: 11,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 16),

                        // Notifications Icon
                        IconButton(
                          icon: const Badge(
                            label: Text('3'),
                            child: Icon(Icons.notifications_outlined),
                          ),
                          onPressed: () {},
                        ),
                      ],
                    ),
                  ),
                ),

                // Dynamic Body View Area
                Expanded(child: activeView),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _getInterfaceTitle(ControlInterface interface) {
    switch (interface) {
      case ControlInterface.enterpriseControlCenter:
        return 'Enterprise Control Center';
      case ControlInterface.executiveCommandCenter:
        return 'Executive Command Center';
      case ControlInterface.operationsConsole:
        return 'Operations Console';
      case ControlInterface.publicPortal:
        return 'Public Portal';
    }
  }
}
