import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import '../providers/control_center_providers.dart';
import '../widgets/metric_card.dart';

class ExecutiveCommandCenterView extends ConsumerWidget {
  const ExecutiveCommandCenterView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final kpis = ref.watch(executiveKpisProvider);
    final theme = Theme.of(context);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Text(
            'Executive Command Center & Strategic KPIs',
            style: theme.textTheme.headlineSmall?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'High-level strategic intelligence, national turnout metrics, regional insights, and platform SLAs.',
            style: theme.textTheme.bodyMedium?.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 24),

          // Strategic KPI Cards
          GridView.count(
            crossAxisCount: 4,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            childAspectRatio: 1.1,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            children: [
              MetricCard(
                title: 'Elections Managed',
                value: '${kpis.totalElectionsManaged}',
                subtitle: 'Lok Sabha & State Assemblies',
                icon: Icons.how_to_vote,
                iconColor: Colors.indigo,
                badgeText: 'Active',
                badgeColor: Colors.blue,
              ),
              const MetricCard(
                title: 'Registered Voters',
                value: '968.8M',
                subtitle: 'National Electoral Roll',
                icon: Icons.groups,
                iconColor: Colors.teal,
                badgeText: '+2.4%',
                badgeColor: Colors.green,
              ),
              MetricCard(
                title: 'Average Voter Turnout',
                value: '${kpis.averageTurnoutPercent}%',
                subtitle: 'National Average Turnout',
                icon: Icons.trending_up,
                iconColor: Colors.green,
                badgeText: 'Record High',
                badgeColor: Colors.green,
              ),
              MetricCard(
                title: 'Platform Uptime SLA',
                value: '${kpis.platformUptimePercent}%',
                subtitle: 'Zero downtime past 90 days',
                icon: Icons.verified,
                iconColor: Colors.amber,
                badgeText: '99.98% SLO',
                badgeColor: Colors.green,
              ),
            ],
          ),
          const SizedBox(height: 32),

          // Regional Insights Table
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
                        'Regional Turnout & Polling Station Performance',
                        style: theme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Chip(
                        label: Text('${kpis.totalPollingBooths} Total Booths'),
                        backgroundColor: theme.colorScheme.primaryContainer,
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: DataTable(
                      columns: const [
                        DataColumn(label: Text('Electoral Region')),
                        DataColumn(label: Text('Polling Booths')),
                        DataColumn(label: Text('Voter Turnout %')),
                        DataColumn(label: Text('Phase Status')),
                      ],
                      rows: const [
                        DataRow(cells: [
                          DataCell(Text('Northern Zone', style: TextStyle(fontWeight: FontWeight.bold))),
                          DataCell(Text('260,000')),
                          DataCell(Text('68.2%')),
                          DataCell(Chip(label: Text('COMPLETED'), backgroundColor: Colors.greenAccent)),
                        ]),
                        DataRow(cells: [
                          DataCell(Text('Southern Zone', style: TextStyle(fontWeight: FontWeight.bold))),
                          DataCell(Text('240,000')),
                          DataCell(Text('71.5%')),
                          DataCell(Chip(label: Text('COMPLETED'), backgroundColor: Colors.greenAccent)),
                        ]),
                        DataRow(cells: [
                          DataCell(Text('Eastern Zone', style: TextStyle(fontWeight: FontWeight.bold))),
                          DataCell(Text('220,000')),
                          DataCell(Text('65.8%')),
                          DataCell(Chip(label: Text('COMPLETED'), backgroundColor: Colors.greenAccent)),
                        ]),
                        DataRow(cells: [
                          DataCell(Text('Western Zone', style: TextStyle(fontWeight: FontWeight.bold))),
                          DataCell(Text('210,000')),
                          DataCell(Text('66.1%')),
                          DataCell(Chip(label: Text('COMPLETED'), backgroundColor: Colors.greenAccent)),
                        ]),
                        DataRow(cells: [
                          DataCell(Text('Central Zone', style: TextStyle(fontWeight: FontWeight.bold))),
                          DataCell(Text('118,000')),
                          DataCell(Text('64.9%')),
                          DataCell(Chip(label: Text('COMPLETED'), backgroundColor: Colors.greenAccent)),
                        ]),
                      ],
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
