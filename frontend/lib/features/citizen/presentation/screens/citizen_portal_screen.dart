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
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Election Intelligence',
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.bold,
            letterSpacing: -0.6,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.tune_outlined, size: 20),
            tooltip: 'Control Center & Analytics',
            onPressed: () => Navigator.of(context).pushNamed('/control-center'),
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Apple/Perplexity Style Hero Search Header
            Container(
              padding: const EdgeInsets.all(24.0),
              decoration: BoxDecoration(
                color: isDark ? const Color(0xFF11131A) : Colors.white,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: isDark ? const Color(0xFF1F2430) : const Color(0xFFE5E7EB),
                  width: 1,
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Explore Indian Election & Candidate Affidavits',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.w700,
                      letterSpacing: -0.6,
                      color: isDark ? Colors.white : const Color(0xFF111827),
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Explore candidate Form 26 disclosures, declared assets, educational backgrounds, and verified public history.',
                    style: TextStyle(
                      fontSize: 14,
                      color: isDark ? const Color(0xFF9CA3AF) : const Color(0xFF6B7280),
                      height: 1.4,
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Perplexity-style Minimal Search Box
                  Container(
                    decoration: BoxDecoration(
                      color: isDark ? const Color(0xFF181A24) : const Color(0xFFF3F4F6),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(
                        color: isDark ? const Color(0xFF2D3342) : const Color(0xFFE5E7EB),
                        width: 1,
                      ),
                    ),
                    child: TextField(
                      decoration: const InputDecoration(
                        hintText: 'Search by candidate, party, or constituency (e.g. Varanasi, INC, Modi)...',
                        hintStyle: TextStyle(fontSize: 14, color: Color(0xFF9CA3AF)),
                        prefixIcon: Icon(Icons.search, size: 20, color: Color(0xFF6B7280)),
                        border: InputBorder.none,
                        contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                      ),
                      onChanged: (val) {
                        ref.read(candidateSearchQueryProvider.notifier).state = val;
                      },
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Notion-Style Non-Partisan Transparency Banner
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: isDark ? const Color(0xFF141A29) : const Color(0xFFEFF6FF),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: isDark ? const Color(0xFF1E293B) : const Color(0xFFDBEAFE),
                ),
              ),
              child: const Row(
                children: [
                  Icon(Icons.shield_outlined, color: Color(0xFF2563EB), size: 18),
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'Non-Partisan Transparency Notice: This platform provides verified public records for Indian citizens. It does not recommend voting for or against any candidate, nor does it rank candidates by opinion.',
                      style: TextStyle(
                        fontSize: 12,
                        color: Color(0xFF1D4ED8),
                        height: 1.3,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Section Header
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Verified Candidate Profiles',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w700,
                    letterSpacing: -0.4,
                  ),
                ),
                Text(
                  '${candidates.length} Records',
                  style: TextStyle(
                    fontSize: 13,
                    color: isDark ? const Color(0xFF9CA3AF) : const Color(0xFF6B7280),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Candidate Profiles Grid
            GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                childAspectRatio: 1.25,
              ),
              itemCount: candidates.length,
              itemBuilder: (context, index) {
                final candidate = candidates[index];
                final isSelected = selectedForComparison.any((c) => c.id == candidate.id);

                return _CandidateCard(
                  candidate: candidate,
                  isSelected: isSelected,
                  onToggleSelect: () {
                    ref.read(comparisonSelectionProvider.notifier).toggleCandidate(candidate);
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
              icon: const Icon(Icons.compare_arrows, size: 20),
              label: Text(
                'Compare (${selectedForComparison.length} Candidates)',
                style: const TextStyle(fontWeight: FontWeight.w600),
              ),
              backgroundColor: const Color(0xFF2563EB),
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
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF11131A) : Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isSelected
              ? const Color(0xFF2563EB)
              : (isDark ? const Color(0xFF1F2430) : const Color(0xFFE5E7EB)),
          width: isSelected ? 2 : 1,
        ),
      ),
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
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                    letterSpacing: -0.3,
                  ),
                ),
                VerificationBadge(type: candidate.verificationStatus),
              ],
            ),
            const SizedBox(height: 4),
            Text(
              '${candidate.partyName} • ${candidate.constituencyName}',
              style: const TextStyle(
                fontSize: 13,
                color: Color(0xFF2563EB),
                fontWeight: FontWeight.w500,
              ),
            ),
            const SizedBox(height: 8),
            const Divider(height: 1),
            const SizedBox(height: 8),
            Wrap(
              alignment: WrapAlignment.spaceBetween,
              children: [
                Text(
                  'Assets: ${candidate.assetsDeclared}',
                  style: TextStyle(
                    fontSize: 12,
                    color: isDark ? const Color(0xFF9CA3AF) : const Color(0xFF4B5563),
                  ),
                ),
                Text(
                  'Cases: ${candidate.criminalCases}',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: candidate.criminalCases > 0
                        ? const Color(0xFFEF4444)
                        : const Color(0xFF10B981),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              height: 36,
              child: OutlinedButton.icon(
                onPressed: onToggleSelect,
                icon: Icon(
                  isSelected ? Icons.check_circle : Icons.add_circle_outline,
                  size: 16,
                  color: isSelected ? const Color(0xFF2563EB) : const Color(0xFF6B7280),
                ),
                label: Text(
                  isSelected ? 'Selected' : 'Compare Candidate',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: isSelected ? const Color(0xFF2563EB) : const Color(0xFF374151),
                  ),
                ),
                style: OutlinedButton.styleFrom(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  side: BorderSide(
                    color: isSelected
                        ? const Color(0xFF2563EB)
                        : (isDark ? const Color(0xFF2D3342) : const Color(0xFFD1D5DB)),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
