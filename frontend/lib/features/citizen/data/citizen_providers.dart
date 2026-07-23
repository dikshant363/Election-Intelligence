import 'package:hooks_riverpod/hooks_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../domain/models/citizen_models.dart';

final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient();
});

final candidatesProvider = FutureProvider<List<CitizenCandidate>>((ref) async {
  final apiClient = ref.watch(apiClientProvider);
  return apiClient.fetchCandidates();
});

final electionsProvider = FutureProvider<List<CitizenElection>>((ref) async {
  final apiClient = ref.watch(apiClientProvider);
  return apiClient.fetchElections();
});

final candidateSearchQueryProvider = StateProvider<String>((ref) => '');

final filteredCandidatesProvider = Provider<List<CitizenCandidate>>((ref) {
  final candidatesAsync = ref.watch(candidatesProvider);
  final query = ref.watch(candidateSearchQueryProvider).toLowerCase();

  return candidatesAsync.when(
    data: (candidates) {
      if (query.isEmpty) return candidates;
      return candidates.where((c) {
        return c.name.toLowerCase().contains(query) ||
            c.partyName.toLowerCase().contains(query) ||
            c.constituencyName.toLowerCase().contains(query);
      }).toList();
    },
    loading: () => [],
    error: (_, __) => [],
  );
});

class ComparisonSelectionNotifier extends StateNotifier<List<CitizenCandidate>> {
  ComparisonSelectionNotifier() : super([]);

  void toggleCandidate(CitizenCandidate candidate) {
    if (state.any((c) => c.id == candidate.id)) {
      state = state.where((c) => c.id != candidate.id).toList();
    } else {
      if (state.length >= 3) {
        // Keep max 3 candidates for side-by-side view
        state = [...state.sublist(1), candidate];
      } else {
        state = [...state, candidate];
      }
    }
  }

  void clear() {
    state = [];
  }
}

final comparisonSelectionProvider =
    StateNotifierProvider<ComparisonSelectionNotifier, List<CitizenCandidate>>((ref) {
  return ComparisonSelectionNotifier();
});
