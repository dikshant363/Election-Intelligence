import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import '../providers/control_center_providers.dart';
import '../widgets/metric_card.dart';

class EnterpriseControlCenterView extends ConsumerWidget {
  const EnterpriseControlCenterView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final health = ref.watch(systemHealthProvider);
    final flags = ref.watch(featureFlagsProvider);
    final flagsNotifier = ref.read(featureFlagsProvider.notifier);
    final auditLogs = ref.watch(auditLogsProvider);
    final theme = Theme.of(context);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Section Title
          Text(
            'Enterprise Infrastructure Telemetry & Control',
            style: theme.textTheme.headlineSmall?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Monitor system resources, toggle feature flags, audit security events, and manage AI model routing.',
            style: theme.textTheme.bodyMedium?.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 24),

          // System Health Metric Cards
          GridView.count(
            crossAxisCount: 4,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            childAspectRatio: 1.1,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            children: [
              MetricCard(
                title: 'CPU Utilization',
                value: '${health.cpuUtilization}%',
                subtitle: 'Apple M4 Server Node',
                icon: Icons.memory,
                iconColor: Colors.blue,
                badgeText: 'Optimal',
                badgeColor: Colors.green,
              ),
              MetricCard(
                title: 'RAM Utilization',
                value: '${health.memoryUtilization}%',
                subtitle: '6.16 GB of 16 GB used',
                icon: Icons.storage,
                iconColor: Colors.purple,
                badgeText: 'Normal',
                badgeColor: Colors.green,
              ),
              MetricCard(
                title: 'Database Pool',
                value: '${health.dbPoolActive} / 15',
                subtitle: 'PostgreSQL 16 active connections',
                icon: Icons.dataset,
                iconColor: Colors.orange,
                badgeText: 'Healthy',
                badgeColor: Colors.green,
              ),
              const MetricCard(
                title: 'Redis Cache Hit Ratio',
                value: '94.6%',
                subtitle: 'Redis 8.8 latency 1.2ms',
                icon: Icons.speed,
                iconColor: Colors.teal,
                badgeText: 'PONG',
                badgeColor: Colors.green,
              ),
            ],
          ),
          const SizedBox(height: 32),

          // Two Column Section: Feature Flags & AI Subsystem Control
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Feature Flags Manager
              Expanded(
                flex: 1,
                child: Card(
                  elevation: 1,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Wrap(
                          alignment: WrapAlignment.spaceBetween,
                          crossAxisAlignment: WrapCrossAlignment.center,
                          children: [
                            Text(
                              'Platform Feature Flags',
                              style: theme.textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Chip(
                              label: Text('${flags.where((f) => f.enabled).length} Enabled'),
                              backgroundColor: Colors.green.withValues(alpha: 0.15),
                              labelStyle: const TextStyle(color: Colors.green, fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        ListView.separated(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: flags.length,
                          separatorBuilder: (context, index) => const Divider(),
                          itemBuilder: (context, index) {
                            final flag = flags[index];
                            return SwitchListTile(
                              title: Text(flag.name, style: const TextStyle(fontWeight: FontWeight.w600)),
                              subtitle: Text(flag.description),
                              value: flag.enabled,
                              activeTrackColor: theme.colorScheme.primary,
                              onChanged: (_) => flagsNotifier.toggleFlag(flag.name),
                            );
                          },
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 24),

              // AI Subsystem Control Center
              Expanded(
                flex: 1,
                child: Card(
                  elevation: 1,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Wrap(
                          alignment: WrapAlignment.spaceBetween,
                          crossAxisAlignment: WrapCrossAlignment.center,
                          children: [
                            Text(
                              'AI Control & Model Routing',
                              style: theme.textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const Chip(
                              label: Text('RAG Healthy'),
                              backgroundColor: Colors.blue,
                              labelStyle: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        const ListTile(
                          leading: Icon(Icons.psychology, color: Colors.indigo),
                          title: Text('Active Provider'),
                          subtitle: Text('OpenAI (Primary) | Fallback: Gemini, Claude, Ollama'),
                          trailing: Chip(label: Text('GPT-4o')),
                        ),
                        const Divider(),
                        const ListTile(
                          leading: Icon(Icons.shield_outlined, color: Colors.teal),
                          title: Text('Safety Guardrails'),
                          subtitle: Text('Pre-LLM & Post-LLM filters enforced'),
                          trailing: Icon(Icons.check_circle, color: Colors.green),
                        ),
                        const Divider(),
                        const ListTile(
                          leading: Icon(Icons.format_quote, color: Colors.amber),
                          title: Text('Citation Attribution System'),
                          subtitle: Text('Strict source evidence requirements'),
                          trailing: Icon(Icons.check_circle, color: Colors.green),
                        ),
                        const Divider(),
                        Padding(
                          padding: const EdgeInsets.only(top: 8.0),
                          child: ElevatedButton.icon(
                            onPressed: () {},
                            icon: const Icon(Icons.tune),
                            label: const Text('Configure Model Parameters'),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 32),

          // Security & Audit Log Table
          Card(
            elevation: 1,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Security & Audit Event Stream',
                        style: theme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      TextButton.icon(
                        onPressed: () {},
                        icon: const Icon(Icons.download),
                        label: const Text('Export Audit Log'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: DataTable(
                      columns: const [
                        DataColumn(label: Text('Timestamp')),
                        DataColumn(label: Text('Actor')),
                        DataColumn(label: Text('Action')),
                        DataColumn(label: Text('Resource')),
                        DataColumn(label: Text('IP Address')),
                        DataColumn(label: Text('Status')),
                      ],
                      rows: auditLogs.map((log) {
                        return DataRow(cells: [
                          DataCell(Text(log.timestamp)),
                          DataCell(Text(log.actor, style: const TextStyle(fontWeight: FontWeight.bold))),
                          DataCell(Text(log.action)),
                          DataCell(Text(log.resource)),
                          DataCell(Text(log.ipAddress)),
                          DataCell(
                            Chip(
                              label: Text(log.status),
                              backgroundColor: Colors.green.withValues(alpha: 0.15),
                              labelStyle: const TextStyle(color: Colors.green, fontSize: 12),
                            ),
                          ),
                        ]);
                      }).toList(),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
