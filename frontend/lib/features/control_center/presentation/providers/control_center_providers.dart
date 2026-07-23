import 'package:hooks_riverpod/hooks_riverpod.dart';
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

final systemHealthProvider = Provider<SystemHealthMetrics>((ref) {
  return SystemHealthMetrics.initial();
});

final executiveKpisProvider = Provider<ExecutiveKpisModel>((ref) {
  return ExecutiveKpisModel.initial();
});

final auditLogsProvider = Provider<List<AuditLogModel>>((ref) {
  return const [
    AuditLogModel(
      id: 'aud-9901',
      timestamp: '2026-07-23T17:22:00Z',
      actor: 'superadmin',
      action: 'UPDATE_FEATURE_FLAG',
      resource: 'feature_flags/enable_rag',
      status: 'SUCCESS',
      ipAddress: '127.0.0.1',
    ),
    AuditLogModel(
      id: 'aud-9902',
      timestamp: '2026-07-23T16:50:00Z',
      actor: 'ops_lead',
      action: 'INGEST_ELECTION_DATA',
      resource: 'etl/batch-8841',
      status: 'SUCCESS',
      ipAddress: '10.0.4.12',
    ),
    AuditLogModel(
      id: 'aud-9903',
      timestamp: '2026-07-23T15:30:00Z',
      actor: 'system',
      action: 'ROTATE_JWT_SECRET',
      resource: 'security/jwt',
      status: 'SUCCESS',
      ipAddress: '127.0.0.1',
    ),
  ];
});

final userAccountsProvider = Provider<List<UserAccountModel>>((ref) {
  return const [
    UserAccountModel(
      id: 'usr-001',
      username: 'superadmin',
      email: 'admin@civiclens.in',
      role: 'Super Administrator',
      isActive: true,
      mfaEnabled: true,
      lastLogin: '2026-07-23T17:30:00Z',
    ),
    UserAccountModel(
      id: 'usr-002',
      username: 'ops_lead',
      email: 'ops@civiclens.in',
      role: 'Election Administrator',
      isActive: true,
      mfaEnabled: true,
      lastLogin: '2026-07-23T16:45:00Z',
    ),
    UserAccountModel(
      id: 'usr-003',
      username: 'ai_eng',
      email: 'ai@civiclens.in',
      role: 'Platform Administrator',
      isActive: true,
      mfaEnabled: true,
      lastLogin: '2026-07-23T15:10:00Z',
    ),
  ];
});
