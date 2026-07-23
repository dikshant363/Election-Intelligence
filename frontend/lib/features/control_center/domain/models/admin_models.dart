import 'package:flutter/foundation.dart';

@immutable
class SystemHealthMetrics {
  final double cpuUtilization;
  final double memoryUtilization;
  final double diskFreeGb;
  final int dbPoolActive;
  final int dbPoolOverflow;
  final double redisLatencyMs;

  const SystemHealthMetrics({
    required this.cpuUtilization,
    required this.memoryUtilization,
    required this.diskFreeGb,
    required this.dbPoolActive,
    required this.dbPoolOverflow,
    required this.redisLatencyMs,
  });

  factory SystemHealthMetrics.initial() {
    return const SystemHealthMetrics(
      cpuUtilization: 14.2,
      memoryUtilization: 38.5,
      diskFreeGb: 57.0,
      dbPoolActive: 5,
      dbPoolOverflow: 0,
      redisLatencyMs: 1.2,
    );
  }
}

@immutable
class FeatureFlagModel {
  final String name;
  final bool enabled;
  final String description;
  final String environment;

  const FeatureFlagModel({
    required this.name,
    required this.enabled,
    required this.description,
    required this.environment,
  });
}

@immutable
class UserAccountModel {
  final String id;
  final String username;
  final String email;
  final String role;
  final bool isActive;
  final bool mfaEnabled;
  final String lastLogin;

  const UserAccountModel({
    required this.id,
    required this.username,
    required this.email,
    required this.role,
    required this.isActive,
    required this.mfaEnabled,
    required this.lastLogin,
  });
}

@immutable
class AuditLogModel {
  final String id;
  final String timestamp;
  final String actor;
  final String action;
  final String resource;
  final String status;
  final String ipAddress;

  const AuditLogModel({
    required this.id,
    required this.timestamp,
    required this.actor,
    required this.action,
    required this.resource,
    required this.status,
    required this.ipAddress,
  });
}

@immutable
class ExecutiveKpisModel {
  final int totalElectionsManaged;
  final int totalVotersRegistered;
  final double averageTurnoutPercent;
  final int totalConstituencies;
  final int totalCandidates;
  final int totalPollingBooths;
  final int aiQueriesProcessed;
  final double platformUptimePercent;

  const ExecutiveKpisModel({
    required this.totalElectionsManaged,
    required this.totalVotersRegistered,
    required this.averageTurnoutPercent,
    required this.totalConstituencies,
    required this.totalCandidates,
    required this.totalPollingBooths,
    required this.aiQueriesProcessed,
    required this.platformUptimePercent,
  });

  factory ExecutiveKpisModel.initial() {
    return const ExecutiveKpisModel(
      totalElectionsManaged: 24,
      totalVotersRegistered: 968800000,
      averageTurnoutPercent: 67.4,
      totalConstituencies: 543,
      totalCandidates: 8420,
      totalPollingBooths: 1048000,
      aiQueriesProcessed: 245000,
      platformUptimePercent: 99.98,
    );
  }
}
