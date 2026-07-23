import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import '../widgets/metric_card.dart';

class OperationsConsoleView extends ConsumerWidget {
  const OperationsConsoleView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Text(
            'Election Operations Console & Data Ingestion',
            style: theme.textTheme.headlineSmall?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Manage election cycles, candidates, constituencies, polling booths, and monitor ETL data import jobs.',
            style: theme.textTheme.bodyMedium?.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 24),

          // Operations Cards
          GridView.count(
            crossAxisCount: 4,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            childAspectRatio: 1.1,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            children: const [
              MetricCard(
                title: 'Active Elections',
                value: '24',
                subtitle: '12 General, 12 Assembly',
                icon: Icons.how_to_vote,
                iconColor: Colors.blue,
                badgeText: 'Active',
                badgeColor: Colors.blue,
              ),
              MetricCard(
                title: 'Constituencies',
                value: '543',
                subtitle: 'Lok Sabha Seats Indexed',
                icon: Icons.map,
                iconColor: Colors.teal,
              ),
              MetricCard(
                title: 'Registered Candidates',
                value: '8,420',
                subtitle: 'Form 26 Affidavits Processed',
                icon: Icons.person_search,
                iconColor: Colors.orange,
              ),
              MetricCard(
                title: 'ETL Pipeline',
                value: 'Batch-8841',
                subtitle: '100% Validated (0 Errors)',
                icon: Icons.sync,
                iconColor: Colors.purple,
                badgeText: 'SUCCESS',
                badgeColor: Colors.green,
              ),
            ],
          ),
          const SizedBox(height: 32),

          // Ingestion Jobs & File Manager
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
                        'Recent ETL Ingestion Batches',
                        style: theme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      ElevatedButton.icon(
                        onPressed: () {},
                        icon: const Icon(Icons.upload),
                        label: const Text('Import CSV / JSON Data'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: DataTable(
                      columns: const [
                        DataColumn(label: Text('Batch ID')),
                        DataColumn(label: Text('Source File')),
                        DataColumn(label: Text('Records')),
                        DataColumn(label: Text('Provenance')),
                        DataColumn(label: Text('Status')),
                      ],
                      rows: const [
                        DataRow(cells: [
                          DataCell(Text('Batch-8841', style: TextStyle(fontWeight: FontWeight.bold))),
                          DataCell(Text('general_election_2026_results.csv')),
                          DataCell(Text('543 seats')),
                          DataCell(Text('ECI Official Feed')),
                          DataCell(Chip(label: Text('LOADED'), backgroundColor: Colors.greenAccent)),
                        ]),
                        DataRow(cells: [
                          DataCell(Text('Batch-8840', style: TextStyle(fontWeight: FontWeight.bold))),
                          DataCell(Text('candidate_affidavits_2026.json')),
                          DataCell(Text('8,420 records')),
                          DataCell(Text('MyNeta Ingestion')),
                          DataCell(Chip(label: Text('LOADED'), backgroundColor: Colors.greenAccent)),
                        ]),
                        DataRow(cells: [
                          DataCell(Text('Batch-8839', style: TextStyle(fontWeight: FontWeight.bold))),
                          DataCell(Text('booth_turnout_phase1.csv')),
                          DataCell(Text('260,000 booths')),
                          DataCell(Text('Chief Electoral Officer')),
                          DataCell(Chip(label: Text('LOADED'), backgroundColor: Colors.greenAccent)),
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
