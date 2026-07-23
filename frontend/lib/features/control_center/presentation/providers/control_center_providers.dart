import 'package:hooks_riverpod/hooks_riverpod.dart';
import '../../../../core/api/api_client.dart';
import '../../domain/models/admin_models.dart';

enum ControlInterface {
  publicPortal,
  operationsConsole,
  enterpriseControlCenter,
  executiveCommandCenter,
}

class ControlInterfaceNotifier extends StateNotifier<ControlInterface> {
  ControlInterfaceNotifier() : super(ControlInterface.enterpriseControlCenter);

  void selectInterface(ControlInterface interface) {
    state = interface;
  }
}

final controlInterfaceProvider =
    StateNotifierProvider<ControlInterfaceNotifier, ControlInterface>((ref) {
  return ControlInterfaceNotifier();
});

class FeatureFlagsNotifier extends StateNotifier<List<FeatureFlagModel>> {
  FeatureFlagsNotifier()
      : super([
          const FeatureFlagModel(
            name: 'enable_rag',
            enabled: true,
            description: 'Enable RAG pipeline for AI queries',
            environment: 'all',
          ),
          const FeatureFlagModel(
            name: 'enable_websockets',
            enabled: true,
            description: 'Enable real-time WebSocket subscriptions',
            environment: 'all',
          ),
          const FeatureFlagModel(
            name: 'enable_sse',
            enabled: true,
            description: 'Enable Server-Sent Events streaming',
            environment: 'all',
          ),
          const FeatureFlagModel(
            name: 'enable_background_workers',
            enabled: true,
            description: 'Enable async task execution workers',
            environment: 'all',
          ),
          const FeatureFlagModel(
            name: 'enable_chaos_testing',
            enabled: false,
            description: 'Enable resilience chaos testing hooks',
            environment: 'staging',
          ),
          const FeatureFlagModel(
            name: 'enable_mfa',
            enabled: true,
            description: 'Enforce Multi-Factor Authentication',
            environment: 'production',
          ),
        ]);

  void toggleFlag(String flagName) {
    state = [
      for (final flag in state)
        if (flag.name == flagName)
          FeatureFlagModel(
            name: flag.name,
            enabled: !flag.enabled,
            description: flag.description,
            environment: flag.environment,
          )
        else
          flag,
    ];
  }
}

final featureFlagsProvider =
    StateNotifierProvider<FeatureFlagsNotifier, List<FeatureFlagModel>>((ref) {
  return FeatureFlagsNotifier();
});

final systemHealthAsyncProvider = FutureProvider<SystemHealthMetrics>((ref) async {
  final apiClient = ApiClient();
  return apiClient.fetchAdminOverview();
});

final systemHealthProvider = Provider<SystemHealthMetrics>((ref) {
  final asyncVal = ref.watch(systemHealthAsyncProvider);
  return asyncVal.when(
    data: (metrics) => metrics,
    loading: () => SystemHealthMetrics.initial(),
    error: (_, __) => SystemHealthMetrics.initial(),
  );
});

final executiveKpisAsyncProvider = FutureProvider<ExecutiveKpisModel>((ref) async {
  final apiClient = ApiClient();
  return apiClient.fetchExecutiveKpis();
});

final executiveKpisProvider = Provider<ExecutiveKpisModel>((ref) {
  final asyncVal = ref.watch(executiveKpisAsyncProvider);
  return asyncVal.when(
    data: (kpis) => kpis,
    loading: () => ExecutiveKpisModel.initial(),
    error: (_, __) => ExecutiveKpisModel.initial(),
  );
});

final auditLogsAsyncProvider = FutureProvider<List<AuditLogModel>>((ref) async {
  final apiClient = ApiClient();
  return apiClient.fetchAuditLogs();
});

final auditLogsProvider = Provider<List<AuditLogModel>>((ref) {
  final asyncVal = ref.watch(auditLogsAsyncProvider);
  return asyncVal.when(
    data: (logs) => logs,
    loading: () => const [],
    error: (_, __) => const [],
  );
});

final userAccountsAsyncProvider = FutureProvider<List<UserAccountModel>>((ref) async {
  final apiClient = ApiClient();
  return apiClient.fetchUserAccounts();
});

final userAccountsProvider = Provider<List<UserAccountModel>>((ref) {
  final asyncVal = ref.watch(userAccountsAsyncProvider);
  return asyncVal.when(
    data: (users) => users,
    loading: () => const [],
    error: (_, __) => const [],
  );
});
