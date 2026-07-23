import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import '../../../../core/widgets/verification_badge.dart';
import '../../data/citizen_providers.dart';
import '../../domain/models/citizen_models.dart';
import 'candidate_comparison_screen.dart';

class CitizenPortalScreen extends ConsumerWidget {
  const CitizenPortalScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final candidates = ref.watch(filteredCandidatesProvider);
    final selectedForComparison = ref.watch(comparisonSelectionProvider);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Election Intelligence — Citizen Portal'),
        actions: [
          IconButton(
            icon: const Icon(Icons.dashboard_customize),
            tooltip: 'Control Center Interface',
            onPressed: () => Navigator.of(context).pushNamed('/control-center'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header Banner
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: theme.colorScheme.primaryContainer,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Icon(
                            Icons.how_to_vote,
                            color: theme.colorScheme.onPrimaryContainer,
                            size: 28,
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Explore Indian Election & Candidate Affidavits',
                                style: theme.textTheme.titleLarge?.copyWith(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                'Publicly available verified records, Form 26 asset disclosures, and election history.',
                                style: theme.textTheme.bodyMedium?.copyWith(
                                  color: theme.colorScheme.onSurfaceVariant,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),

                    // Search Input Box
                    TextField(
                      decoration: InputDecoration(
                        hintText: 'Search candidate name, party, or constituency (e.g. Modi, Varanasi, INC)...',
                        prefixIcon: const Icon(Icons.search),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      onChanged: (val) {
                        ref
                            .read(candidateSearchQueryProvider.notifier)
                            .state = val;
                      },
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Policy Neutrality & Data Provenance Disclaimer
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.blue.withValues(alpha: 0.08),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: Colors.blue.withValues(alpha: 0.2),
                ),
              ),
              child: const Row(
                children: [
                  Icon(Icons.shield_outlined, color: Colors.blue, size: 20),
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'Non-Partisan Transparency Notice: This platform provides verified public records for Indian citizens. It does not recommend voting for or against any candidate, nor does it rank candidates by opinion.',
                      style: TextStyle(fontSize: 12, color: Colors.blueAccent),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Section Title & Counter
            Wrap(
              alignment: WrapAlignment.spaceBetween,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                Text(
                  'Candidate Profiles & Public Affidavits',
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  '${candidates.length} Profiles Available',
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Candidate Cards Grid
            GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                childAspectRatio: 1.4,
              ),
              itemCount: candidates.length,
              itemBuilder: (context, index) {
                final candidate = candidates[index];
                final isSelected = selectedForComparison
                    .any((c) => c.id == candidate.id);

                return _CandidateCard(
                  candidate: candidate,
                  isSelected: isSelected,
                  onToggleSelect: () {
                    ref
                        .read(comparisonSelectionProvider.notifier)
                        .toggleCandidate(candidate);
                  },
                );
              },
            ),
          ],
        ),
      ),
      floatingActionButton: selectedForComparison.isNotEmpty
          ? FloatingActionButton.extended(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => const CandidateComparisonScreen(),
                  ),
                );
              },
              icon: const Icon(Icons.compare_arrows),
              label: Text('Compare (${selectedForComparison.length} Selected)'),
              backgroundColor: theme.colorScheme.primary,
            )
          : null,
    );
  }
}

class _CandidateCard extends StatelessWidget {
  final CitizenCandidate candidate;
  final bool isSelected;
  final VoidCallback onToggleSelect;

  const _CandidateCard({
    required this.candidate,
    required this.isSelected,
    required this.onToggleSelect,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      elevation: isSelected ? 4 : 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: isSelected
            ? BorderSide(color: theme.colorScheme.primary, width: 2)
            : BorderSide.none,
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Wrap(
                alignment: WrapAlignment.spaceBetween,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  Text(
                    candidate.name,
                    style: theme.textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  VerificationBadge(type: candidate.verificationStatus),
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
              const Divider(height: 16),
              Wrap(
                alignment: WrapAlignment.spaceBetween,
                children: [
                  Text('Assets: ${candidate.assetsDeclared}', style: theme.textTheme.bodySmall),
                  const SizedBox(width: 8),
                  Text('Cases: ${candidate.criminalCases}',
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: candidate.criminalCases > 0 ? Colors.red : Colors.green,
                        fontWeight: FontWeight.bold,
                      )),
                ],
              ),
              const SizedBox(height: 12),
              OutlinedButton.icon(
                onPressed: onToggleSelect,
                icon: Icon(
                  isSelected ? Icons.check_box : Icons.add_circle_outline,
                  size: 16,
                ),
                label: Text(isSelected ? 'Selected' : 'Compare Candidate'),
                style: OutlinedButton.styleFrom(
                  minimumSize: const Size.fromHeight(36),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
