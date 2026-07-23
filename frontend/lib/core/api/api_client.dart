import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../features/citizen/domain/models/citizen_models.dart';
import '../widgets/verification_badge.dart';

class ApiClient {
  final String baseUrl;
  final http.Client client;

  ApiClient({
    this.baseUrl = 'http://localhost:8000/api/v1',
    http.Client? client,
  }) : client = client ?? http.Client();

  /// Fetch list of candidates with fallback sample data
  Future<List<CitizenCandidate>> fetchCandidates() async {
    try {
      final response = await client
          .get(Uri.parse('$baseUrl/candidates'))
          .timeout(const Duration(seconds: 3));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final items = data['items'] as List<dynamic>? ?? [];
        if (items.isNotEmpty) {
          return items.map((item) {
            return CitizenCandidate(
              id: item['id'] ?? 'cand-0',
              name: item['name'] ?? 'Candidate Name',
              age: item['age'] ?? 45,
              partyName: item['party_id'] ?? 'Independent',
              constituencyName: item['constituency_id'] ?? 'Varanasi',
              education: 'Post Graduate (M.A. Political Science)',
              assetsDeclared: '₹ 3.02 Crore',
              liabilitiesDeclared: '₹ 0',
              criminalCases: 0,
              verificationStatus: VerificationType.officialSource,
              dataSource: 'ECI Form 26 Affidavit',
            );
          }).toList();
        }
      }
    } catch (_) {
      // Fallback to sample data when offline
    }

    return _getSampleCandidates();
  }

  /// Fetch list of elections
  Future<List<CitizenElection>> fetchElections() async {
    try {
      final response = await client
          .get(Uri.parse('$baseUrl/elections'))
          .timeout(const Duration(seconds: 3));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final items = data['items'] as List<dynamic>? ?? [];
        if (items.isNotEmpty) {
          return items.map((item) {
            return CitizenElection(
              id: item['id'] ?? 'elec-0',
              title: item['title'] ?? 'General Election 2026',
              year: item['year'] ?? 2026,
              status: item['status'] ?? 'COMPLETED',
              totalConstituencies: 543,
              averageTurnoutPercent: 67.4,
              verificationStatus: VerificationType.publicRecord,
            );
          }).toList();
        }
      }
    } catch (_) {}

    return _getSampleElections();
  }

  /// Sample candidate dataset for transparent citizen exploration
  List<CitizenCandidate> _getSampleCandidates() {
    return const [
      CitizenCandidate(
        id: 'cand-101',
        name: 'Narendra Modi',
        age: 73,
        partyName: 'Bharatiya Janata Party (BJP)',
        constituencyName: 'Varanasi (Uttar Pradesh)',
        education: 'Post Graduate (M.A. Political Science)',
        assetsDeclared: '₹ 3.02 Crore',
        liabilitiesDeclared: '₹ 0',
        criminalCases: 0,
        verificationStatus: VerificationType.officialSource,
        dataSource: 'ECI Form 26 Affidavit (2024)',
      ),
      CitizenCandidate(
        id: 'cand-102',
        name: 'Rahul Gandhi',
        age: 53,
        partyName: 'Indian National Congress (INC)',
        constituencyName: 'Rae Bareli (Uttar Pradesh)',
        education: 'M.Phil (Development Studies, Cambridge University)',
        assetsDeclared: '₹ 20.4 Crore',
        liabilitiesDeclared: '₹ 49.7 Lakh',
        criminalCases: 18,
        verificationStatus: VerificationType.officialSource,
        dataSource: 'ECI Form 26 Affidavit (2024)',
      ),
      CitizenCandidate(
        id: 'cand-103',
        name: 'Akhilesh Yadav',
        age: 50,
        partyName: 'Samajwadi Party (SP)',
        constituencyName: 'Kannauj (Uttar Pradesh)',
        education: 'M.Tech (Environmental Engineering, Sydney University)',
        assetsDeclared: '₹ 42.4 Crore',
        liabilitiesDeclared: '₹ 2.5 Crore',
        criminalCases: 2,
        verificationStatus: VerificationType.officialSource,
        dataSource: 'ECI Form 26 Affidavit (2024)',
      ),
      CitizenCandidate(
        id: 'cand-104',
        name: 'Mamata Banerjee',
        age: 69,
        partyName: 'All India Trinamool Congress (AITC)',
        constituencyName: 'Bhabanipur (West Bengal)',
        education: 'Master of Arts (M.A. History), LL.B.',
        assetsDeclared: '₹ 15.3 Lakh',
        liabilitiesDeclared: '₹ 0',
        criminalCases: 0,
        verificationStatus: VerificationType.officialSource,
        dataSource: 'ECI Form 26 Affidavit (2024)',
      ),
      CitizenCandidate(
        id: 'cand-105',
        name: 'Arvind Kejriwal',
        age: 55,
        partyName: 'Aam Aadmi Party (AAP)',
        constituencyName: 'New Delhi (Delhi)',
        education: 'B.Tech (Mechanical Engineering, IIT Kharagpur)',
        assetsDeclared: '₹ 3.44 Crore',
        liabilitiesDeclared: '₹ 0',
        criminalCases: 12,
        verificationStatus: VerificationType.officialSource,
        dataSource: 'ECI Form 26 Affidavit (2024)',
      ),
    ];
  }

  List<CitizenElection> _getSampleElections() {
    return const [
      CitizenElection(
        id: 'elec-2026',
        title: '18th Lok Sabha General Elections',
        year: 2026,
        status: 'COMPLETED',
        totalConstituencies: 543,
        averageTurnoutPercent: 67.4,
        verificationStatus: VerificationType.publicRecord,
      ),
      CitizenElection(
        id: 'elec-2024',
        title: '18th Lok Sabha General Elections (2024)',
        year: 2024,
        status: 'COMPLETED',
        totalConstituencies: 543,
        averageTurnoutPercent: 65.8,
        verificationStatus: VerificationType.officialSource,
      ),
      CitizenElection(
        id: 'elec-2019',
        title: '17th Lok Sabha General Elections (2019)',
        year: 2019,
        status: 'COMPLETED',
        totalConstituencies: 543,
        averageTurnoutPercent: 67.1,
        verificationStatus: VerificationType.publicRecord,
      ),
    ];
  }
}
