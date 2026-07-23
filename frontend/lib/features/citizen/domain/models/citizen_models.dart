import 'package:flutter/foundation.dart';
import '../../../../core/widgets/verification_badge.dart';

@immutable
class CitizenCandidate {
  final String id;
  final String name;
  final int age;
  final String partyName;
  final String constituencyName;
  final String education;
  final String assetsDeclared;
  final String liabilitiesDeclared;
  final int criminalCases;
  final VerificationType verificationStatus;
  final String dataSource;

  const CitizenCandidate({
    required this.id,
    required this.name,
    required this.age,
    required this.partyName,
    required this.constituencyName,
    required this.education,
    required this.assetsDeclared,
    required this.liabilitiesDeclared,
    required this.criminalCases,
    required this.verificationStatus,
    required this.dataSource,
  });
}

@immutable
class CitizenConstituency {
  final String id;
  final String name;
  final String state;
  final int totalVoters;
  final int pollingBoothsCount;
  final VerificationType verificationStatus;

  const CitizenConstituency({
    required this.id,
    required this.name,
    required this.state,
    required this.totalVoters,
    required this.pollingBoothsCount,
    required this.verificationStatus,
  });
}

@immutable
class CitizenParty {
  final String id;
  final String name;
  final String symbol;
  final String partyType;
  final int seatsContested;
  final VerificationType verificationStatus;

  const CitizenParty({
    required this.id,
    required this.name,
    required this.symbol,
    required this.partyType,
    required this.seatsContested,
    required this.verificationStatus,
  });
}

@immutable
class CitizenElection {
  final String id;
  final String title;
  final int year;
  final String status;
  final int totalConstituencies;
  final double averageTurnoutPercent;
  final VerificationType verificationStatus;

  const CitizenElection({
    required this.id,
    required this.title,
    required this.year,
    required this.status,
    required this.totalConstituencies,
    required this.averageTurnoutPercent,
    required this.verificationStatus,
  });
}
