import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import '../../../../core/widgets/verification_badge.dart';
import '../../data/citizen_providers.dart';

class CandidateComparisonScreen extends ConsumerWidget {
  const CandidateComparisonScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final selectedCandidates = ref.watch(comparisonSelectionProvider);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Neutral Candidate Affidavit Comparison'),
        actions: [
          if (selectedCandidates.isNotEmpty)
            TextButton.icon(
              onPressed: () {
                ref.read(comparisonSelectionProvider.notifier).clear();
              },
              icon: const Icon(Icons.clear_all),
              label: const Text('Clear Comparison'),
            ),
        ],
      ),
      body: selectedCandidates.isEmpty
          ? Center(
              child: Padding(
                padding: const EdgeInsets.all(32.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.compare_arrows,
                      size: 64,
                      color: theme.colorScheme.primary.withValues(alpha: 0.5),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'No Candidates Selected for Comparison',
                      style: theme.textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Select up to 3 candidates from the Citizen Portal to view side-by-side verified Form 26 affidavit disclosures.',
                      textAlign: TextAlign.center,
                      style: theme.textTheme.bodyMedium?.copyWith(
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
                    ),
                    const SizedBox(height: 24),
                    ElevatedButton.icon(
                      onPressed: () => Navigator.of(context).pop(),
                      icon: const Icon(Icons.arrow_back),
                      label: const Text('Return to Candidate Explorer'),
                    ),
                  ],
                ),
              ),
            )
          : SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Neutral Disclaimer Banner
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: theme.colorScheme.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: theme.colorScheme.outlineVariant,
                      ),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.info_outline, color: Colors.blue),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            'Neutral Public Information Comparison: All data presented below is extracted directly from official Election Commission of India (ECI) Form 26 candidate affidavits. CivicLens India does not rank, rate, or express opinions on candidates.',
                            style: theme.textTheme.bodySmall?.copyWith(
                              color: theme.colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Comparison Table
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: selectedCandidates.map((candidate) {
                        return Container(
                          width: 320,
                          margin: const EdgeInsets.only(right: 16),
                          child: Card(
                            elevation: 2,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(20.0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  // Header Name & Party
                                  Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    children: [
                                      Expanded(
                                        child: Text(
                                          candidate.name,
                                          style: theme.textTheme.titleMedium
                                              ?.copyWith(
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ),
                                      VerificationBadge(
                                        type: candidate.verificationStatus,
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    candidate.partyName,
                                    style: theme.textTheme.bodySmall?.copyWith(
                                      color: theme.colorScheme.primary,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                  Text(
                                    candidate.constituencyName,
                                    style: theme.textTheme.labelSmall?.copyWith(
                                      color: theme.colorScheme.onSurfaceVariant,
                                    ),
                                  ),
                                  const Divider(height: 24),

                                  // Attribute Rows
                                  _AttrRow(
                                    label: 'Age',
                                    value: '${candidate.age} Years',
                                  ),
                                  _AttrRow(
                                    label: 'Education',
                                    value: candidate.education,
                                  ),
                                  _AttrRow(
                                    label: 'Declared Gross Assets',
                                    value: candidate.assetsDeclared,
                                    highlight: true,
                                  ),
                                  _AttrRow(
                                    label: 'Declared Liabilities',
                                    value: candidate.liabilitiesDeclared,
                                  ),
                                  _AttrRow(
                                    label: 'Declared Criminal Cases',
                                    value: '${candidate.criminalCases} Cases',
                                    valueColor: candidate.criminalCases > 0
                                        ? Colors.red
                                        : Colors.green,
                                  ),
                                  const Divider(height: 24),

                                  // Data Source Tag
                                  Text(
                                    'Source: ${candidate.dataSource}',
                                    style: theme.textTheme.labelSmall?.copyWith(
                                      color: theme.colorScheme.onSurfaceVariant
                                          .withValues(alpha: 0.8),
                                      fontStyle: FontStyle.italic,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}

class _AttrRow extends StatelessWidget {
  final String label;
  final String value;
  final bool highlight;
  final Color? valueColor;

  const _AttrRow({
    required this.label,
    required this.value,
    this.highlight = false,
    this.valueColor,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: theme.textTheme.labelSmall?.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            value,
            style: theme.textTheme.bodyMedium?.copyWith(
              fontWeight: highlight ? FontWeight.bold : FontWeight.w500,
              color: valueColor ?? theme.colorScheme.onSurface,
            ),
          ),
        ],
      ),
    );
  }
}
