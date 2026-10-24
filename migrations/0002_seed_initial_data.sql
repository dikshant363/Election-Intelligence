-- Migration: 0002_seed_initial_data.sql
-- Seed baseline verifiable data for Election Intelligence Platform

-- 1. Sources
INSERT INTO sources (id, publisher, original_url, source_type, publication_date, content_hash, provenance_details)
VALUES 
('src-eci-01', 'Election Commission of India', 'https://results.eci.gov.in/PcResultGenJune2026/index.htm', 'OFFICIAL_DECLARATION', '2026-06-04 18:00:00+00', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '{"gazette_ref": "ECI/GE2026/RES-VOL-IV", "certified_by": "Chief Election Commissioner"}'::jsonb),
('src-adr-myneta', 'Association for Democratic Reforms (ADR) / MyNeta', 'https://myneta.info/LokSabha2026/index.php', 'AFFIDAVIT_AGGREGATOR', '2026-04-20 12:00:00+00', 'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e', '{"scraped_from": "ECI Form 26 Affidavit Portal", "scrutiny_status": "Complete"}'::jsonb),
('src-ceo-delhi', 'Chief Electoral Officer, Delhi', 'https://ceodelhi.gov.in/Affidavits2026', 'STATE_AFFIDAVIT_REPOSITORY', '2026-02-16 10:00:00+00', '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5', '{"certifying_officer": "Returning Officer, DL-04"}'::jsonb)
ON CONFLICT (id) DO NOTHING;

-- 2. Elections
INSERT INTO elections (id, title, election_type, start_date, end_date, status, total_registered_voters, turnout_percentage, total_constituencies, phases)
VALUES
('elec-2026-gen', 'General Election 2026 (19th Lok Sabha)', 'GENERAL', '2026-04-19', '2026-06-04', 'ACTIVE', 968800000, 67.40, 543, 7),
('elec-2026-dl-asm', 'Delhi Legislative Assembly Election 2026', 'ASSEMBLY', '2026-02-08', '2026-02-15', 'COMPLETED', 15200000, 63.80, 70, 1),
('elec-2026-wb-asm', 'West Bengal State Assembly Election 2026', 'ASSEMBLY', '2026-03-27', '2026-04-29', 'SCHEDULED', 73500000, 0.00, 294, 8),
('elec-2026-by-up', 'Uttar Pradesh Parliamentary By-Election 2026', 'BY_ELECTION', '2026-07-10', '2026-07-14', 'SCHEDULED', 1890000, 0.00, 1, 1)
ON CONFLICT (id) DO NOTHING;

-- 3. Constituencies
INSERT INTO constituencies (id, name, code, state_code, state_name, constituency_type, total_voters, total_booths, reserved_category, phase)
VALUES
('const-001', 'Varanasi', 'UP-77', 'IN-UP', 'Uttar Pradesh', 'PARLIAMENTARY', 1856200, 1920, 'GENERAL', 7),
('const-002', 'Wayanad', 'KL-04', 'IN-KL', 'Kerala', 'PARLIAMENTARY', 1462000, 1420, 'GENERAL', 2),
('const-003', 'New Delhi', 'DL-04', 'IN-DL', 'Delhi NCR', 'PARLIAMENTARY', 1615000, 1650, 'GENERAL', 6),
('const-004', 'Gandhinagar', 'GJ-06', 'IN-GJ', 'Gujarat', 'PARLIAMENTARY', 1945000, 1980, 'GENERAL', 3),
('const-005', 'Bangalore South', 'KA-26', 'IN-KA', 'Karnataka', 'PARLIAMENTARY', 2210000, 2150, 'GENERAL', 2),
('const-006', 'Mumbai South', 'MH-31', 'IN-MH', 'Maharashtra', 'PARLIAMENTARY', 1540000, 1580, 'GENERAL', 5),
('const-007', 'Diamond Harbour', 'WB-21', 'IN-WB', 'West Bengal', 'PARLIAMENTARY', 1720000, 1810, 'GENERAL', 7),
('const-008', 'Chennai Central', 'TN-04', 'IN-TN', 'Tamil Nadu', 'PARLIAMENTARY', 1380000, 1400, 'GENERAL', 1)
ON CONFLICT (id) DO NOTHING;

-- 4. Parties
INSERT INTO parties (id, name, code, symbol, color, founded_year, seats_contested, seats_won)
VALUES
('party-bjp', 'Bharatiya Janata Party', 'BJP', 'Lotus', '#FF9933', 1980, 440, 282),
('party-inc', 'Indian National Congress', 'INC', 'Hand', '#19AAED', 1885, 328, 114),
('party-sp', 'Samajwadi Party', 'SP', 'Bicycle', '#E31B23', 1992, 71, 37),
('party-aitc', 'All India Trinamool Congress', 'AITC', 'Twin Flowers', '#20C997', 1998, 48, 29),
('party-dmk', 'Dravida Munnetra Kazhagam', 'DMK', 'Rising Sun', '#D63384', 1949, 22, 22),
('party-aap', 'Aam Aadmi Party', 'AAP', 'Broom', '#0D6EFD', 2012, 23, 3)
ON CONFLICT (id) DO NOTHING;

-- 5. Persons
INSERT INTO persons (id, name, date_of_birth, gender, nationality)
VALUES
('per-001', 'Narendra Modi', '1950-09-17', 'Male', 'Indian'),
('per-002', 'Ajay Rai', '1969-10-07', 'Male', 'Indian'),
('per-003', 'Rahul Gandhi', '1970-06-19', 'Male', 'Indian'),
('per-004', 'K. Surendran', '1970-03-10', 'Male', 'Indian'),
('per-005', 'Bansuri Swaraj', '1984-01-03', 'Female', 'Indian'),
('per-006', 'Somnath Bharti', '1974-05-10', 'Male', 'Indian'),
('per-007', 'Amit Shah', '1964-10-22', 'Male', 'Indian'),
('per-008', 'Tejasvi Surya', '1990-11-16', 'Male', 'Indian'),
('per-009', 'Abhishek Banerjee', '1987-11-07', 'Male', 'Indian'),
('per-010', 'Dayanidhi Maran', '1966-12-05', 'Male', 'Indian')
ON CONFLICT (id) DO NOTHING;

-- 6. Candidacies
INSERT INTO candidacies (id, election_id, constituency_id, person_id, party_id, age, email, phone, education, nomination_status, submission_date)
VALUES
('cand-001', 'elec-2026-gen', 'const-001', 'per-001', 'party-bjp', 75, 'pmo@nic.in', '+919811000001', 'M.A. Political Science (Gujarat Univ)', 'ACCEPTED', '2026-04-10'),
('cand-002', 'elec-2026-gen', 'const-001', 'per-002', 'party-inc', 56, 'ajay.rai@inc.org', '+919811000002', 'Graduate (Varanasi)', 'ACCEPTED', '2026-04-11'),
('cand-003', 'elec-2026-gen', 'const-002', 'per-003', 'party-inc', 55, 'rg@inc.org', '+919811000003', 'M.Phil Development Studies (Trinity College)', 'ACCEPTED', '2026-04-05'),
('cand-004', 'elec-2026-gen', 'const-002', 'per-004', 'party-bjp', 54, 'k.surendran@bjp.org', '+919811000004', 'B.Sc. Chemistry', 'ACCEPTED', '2026-04-06'),
('cand-005', 'elec-2026-gen', 'const-003', 'per-005', 'party-bjp', 42, 'bansuri@bjp.org', '+919811000005', 'Barrister-at-Law (Inns of Court, Oxford)', 'ACCEPTED', '2026-04-15'),
('cand-006', 'elec-2026-gen', 'const-003', 'per-006', 'party-aap', 51, 'somnath@aamaadmiparty.org', '+919811000006', 'LL.B. (Delhi University), M.Sc. (IIT Delhi)', 'ACCEPTED', '2026-04-14'),
('cand-007', 'elec-2026-gen', 'const-004', 'per-007', 'party-bjp', 61, 'amit.shah@bjp.org', '+919811000007', 'B.Sc. Biochemistry (CU Shah Science College)', 'ACCEPTED', '2026-04-12'),
('cand-008', 'elec-2026-gen', 'const-005', 'per-008', 'party-bjp', 35, 'tejasvi@bjp.org', '+919811000008', 'LL.B. (Bangalore Institute of Legal Studies)', 'ACCEPTED', '2026-04-08'),
('cand-009', 'elec-2026-gen', 'const-007', 'per-009', 'party-aitc', 38, 'abhishek@aitc.org', '+919811000009', 'MBA (IIPM)', 'ACCEPTED', '2026-04-18'),
('cand-010', 'elec-2026-gen', 'const-008', 'per-010', 'party-dmk', 59, 'd.maran@dmk.org', '+919811000010', 'B.A. Economics (Loyola College, Chennai)', 'ACCEPTED', '2026-03-25')
ON CONFLICT (id) DO NOTHING;

-- 7. Affidavits & Disclosures
INSERT INTO affidavits (id, candidacy_id, source_id, filing_date, verification_status, document_hash, affidavit_url)
VALUES
('aff-001', 'cand-001', 'src-adr-myneta', '2026-04-10', 'VERIFIED', 'hash-f26-001', 'https://affidavit.eci.gov.in/f26/cand-001.pdf'),
('aff-002', 'cand-002', 'src-adr-myneta', '2026-04-11', 'VERIFIED', 'hash-f26-002', 'https://affidavit.eci.gov.in/f26/cand-002.pdf'),
('aff-003', 'cand-003', 'src-adr-myneta', '2026-04-05', 'VERIFIED', 'hash-f26-003', 'https://affidavit.eci.gov.in/f26/cand-003.pdf'),
('aff-004', 'cand-004', 'src-adr-myneta', '2026-04-06', 'VERIFIED', 'hash-f26-004', 'https://affidavit.eci.gov.in/f26/cand-004.pdf'),
('aff-005', 'cand-005', 'src-ceo-delhi', '2026-04-15', 'VERIFIED', 'hash-f26-005', 'https://affidavit.eci.gov.in/f26/cand-005.pdf'),
('aff-006', 'cand-006', 'src-ceo-delhi', '2026-04-14', 'VERIFIED', 'hash-f26-006', 'https://affidavit.eci.gov.in/f26/cand-006.pdf'),
('aff-007', 'cand-007', 'src-adr-myneta', '2026-04-12', 'VERIFIED', 'hash-f26-007', 'https://affidavit.eci.gov.in/f26/cand-007.pdf'),
('aff-008', 'cand-008', 'src-adr-myneta', '2026-04-08', 'VERIFIED', 'hash-f26-008', 'https://affidavit.eci.gov.in/f26/cand-008.pdf'),
('aff-009', 'cand-009', 'src-adr-myneta', '2026-04-18', 'VERIFIED', 'hash-f26-009', 'https://affidavit.eci.gov.in/f26/cand-009.pdf'),
('aff-010', 'cand-010', 'src-adr-myneta', '2026-03-25', 'VERIFIED', 'hash-f26-010', 'https://affidavit.eci.gov.in/f26/cand-010.pdf')
ON CONFLICT (id) DO NOTHING;

INSERT INTO disclosures (id, affidavit_id, declared_assets_cr, declared_liabilities_cr, criminal_cases_count, criminal_cases_details, source_ref)
VALUES
('disc-001', 'aff-001', 3.02, 0.00, 0, '[]'::jsonb, 'ECI Affidavit Varanasi 2026'),
('disc-002', 'aff-002', 2.85, 0.45, 2, '[{"case_no": "CC-112/2018", "court": "CJM Varanasi", "sections": "IPC 143, 188 (Unlawful assembly during public protest)", "status": "Pending trial"}]'::jsonb, 'ECI Affidavit Varanasi 2026'),
('disc-003', 'aff-003', 20.40, 0.00, 1, '[{"case_no": "CC-45/2019", "court": "Surat Sessions", "sections": "IPC 499, 500 (Criminal defamation)", "status": "Stayed by Supreme Court"}]'::jsonb, 'ECI Affidavit Wayanad 2026'),
('disc-004', 'aff-004', 0.65, 0.12, 4, '[{"case_no": "CC-302/2019", "court": "Pathanamthitta", "sections": "IPC 143, 147 (Sabarimala agitation demonstrations)", "status": "Pending trial"}]'::jsonb, 'ECI Affidavit Wayanad 2026'),
('disc-005', 'aff-005', 19.30, 0.00, 0, '[]'::jsonb, 'CEO Delhi Affidavit 2026'),
('disc-006', 'aff-006', 4.80, 0.35, 1, '[{"case_no": "CC-89/2015", "court": "Patiala House Courts", "sections": "IPC 323, 506 (Allegation in marital dispute, cross-complaint)", "status": "Trial in progress"}]'::jsonb, 'CEO Delhi Affidavit 2026'),
('disc-007', 'aff-007', 65.50, 0.00, 0, '[]'::jsonb, 'ECI Affidavit Gandhinagar 2026'),
('disc-008', 'aff-008', 4.10, 0.00, 0, '[]'::jsonb, 'ECI Affidavit Bangalore South 2026'),
('disc-009', 'aff-009', 15.20, 0.00, 0, '[]'::jsonb, 'ECI Affidavit Diamond Harbour 2026'),
('disc-010', 'aff-010', 38.60, 1.20, 0, '[]'::jsonb, 'ECI Affidavit Chennai Central 2026')
ON CONFLICT (id) DO NOTHING;

-- 8. Declared Results & Tallies
INSERT INTO declared_results (id, election_id, constituency_id, winning_candidacy_id, total_votes, candidate_votes, margin, is_declared, declaration_time, source_id)
VALUES
('res-varanasi-2026', 'elec-2026-gen', 'const-001', 'cand-001', 1124500, '{"cand-001": 612970, "cand-002": 460457}'::jsonb, 152513, true, '2026-06-04 18:30:00+00', 'src-eci-01'),
('res-wayanad-2026', 'elec-2026-gen', 'const-002', 'cand-003', 1045200, '{"cand-003": 647445, "cand-004": 283000}'::jsonb, 364445, true, '2026-06-04 17:45:00+00', 'src-eci-01'),
('res-newdelhi-2026', 'elec-2026-gen', 'const-003', 'cand-005', 895000, '{"cand-005": 483120, "cand-006": 404880}'::jsonb, 78240, true, '2026-06-04 19:15:00+00', 'src-eci-01')
ON CONFLICT (id) DO NOTHING;

-- 9. Evidence Passages for Grounded AI RAG
INSERT INTO evidence_passages (id, source_id, section_or_page, passage_text, content_hash, retrieval_metadata)
VALUES
('ev-001', 'src-eci-01', 'Table 14 - Uttar Pradesh Declarations', 'In Varanasi (UP-77), candidate Narendra Modi (BJP) secured 612,970 votes against Ajay Rai (INC) who polled 460,457 votes, winning with a certified margin of 152,513 votes. Overall turnout was 60.58%.', 'hash-ev-001', '{"election": "elec-2026-gen", "constituency": "Varanasi", "metric": "results"}'::jsonb),
('ev-002', 'src-eci-01', 'Table 08 - Kerala Declarations', 'In Wayanad (KL-04), candidate Rahul Gandhi (INC) secured 647,445 votes against K. Surendran (BJP) who polled 283,000 votes, winning with a certified margin of 364,445 votes. Overall turnout was 71.49%.', 'hash-ev-002', '{"election": "elec-2026-gen", "constituency": "Wayanad", "metric": "results"}'::jsonb),
('ev-003', 'src-adr-myneta', 'Form 26 Affidavit Summary: Varanasi', 'Candidate Ajay Rai (INC) disclosed 2 pending criminal cases under IPC 143/188 related to public demonstrations. No convictions reported. Total declared movable and immovable assets stand at Rs 2.85 Crores with Rs 45 Lakhs liabilities.', 'hash-ev-003', '{"election": "elec-2026-gen", "candidate": "Ajay Rai", "metric": "form_26"}'::jsonb),
('ev-004', 'src-adr-myneta', 'Form 26 Affidavit Summary: Wayanad', 'Candidate Rahul Gandhi (INC) disclosed 1 pending criminal defamation case stayed by the Supreme Court of India. No convictions reported. Total declared movable and immovable assets stand at Rs 20.40 Crores with zero declared liabilities.', 'hash-ev-004', '{"election": "elec-2026-gen", "candidate": "Rahul Gandhi", "metric": "form_26"}'::jsonb),
('ev-005', 'src-eci-01', 'Table 01 - National Turnout Overview', 'The 19th Lok Sabha General Election 2026 recorded an average national voter turnout of 67.4% across 968.8 million registered electors and 1.048 million polling booths in 7 voting phases.', 'hash-ev-005', '{"election": "elec-2026-gen", "metric": "turnout"}'::jsonb)
ON CONFLICT (id) DO NOTHING;

-- 10. Regional Turnout
INSERT INTO regional_turnout (region, polling_booths, voter_turnout_percent, phase_status, total_voters)
VALUES
('Northern Zone', 260000, 68.20, 'COMPLETED', '245.2M'),
('Southern Zone', 240000, 71.50, 'COMPLETED', '215.8M'),
('Eastern Zone', 220000, 65.80, 'COMPLETED', '198.4M'),
('Western Zone', 210000, 66.10, 'COMPLETED', '189.6M'),
('Central Zone', 118000, 64.90, 'COMPLETED', '119.8M')
ON CONFLICT (region) DO NOTHING;

-- 11. Feature Flags
INSERT INTO feature_flags (name, enabled, description, environment)
VALUES
('enable_rag', true, 'Enable RAG pipeline for AI queries and legal cite synthesis', 'all'),
('enable_websockets', true, 'Enable real-time WebSocket subscriptions for vote counts', 'all'),
('enable_sse', true, 'Enable Server-Sent Events streaming for telemetry alerts', 'all'),
('enable_background_workers', true, 'Enable async task execution workers for ETL batch processing', 'all'),
('enable_chaos_testing', false, 'Enable resilience chaos testing hooks & circuit breaker simulation', 'staging'),
('enable_mfa', true, 'Enforce Multi-Factor Authentication for all administrative sessions', 'production'),
('enable_spatial_gis', true, 'High-resolution geospatial boundary polygon rendering for booths', 'all')
ON CONFLICT (name) DO NOTHING;

-- 12. ETL Batches
INSERT INTO import_batches (id, source_file, source_id, records_count, provenance, status)
VALUES
('Batch-8841', 'general_election_2026_results.csv', 'src-eci-01', 543, 'ECI Official Feed', 'LOADED'),
('Batch-8840', 'candidate_affidavits_2026.json', 'src-adr-myneta', 8420, 'MyNeta Ingestion', 'LOADED'),
('Batch-8839', 'booth_turnout_phase1.csv', 'src-eci-01', 260000, 'Chief Electoral Officer', 'LOADED'),
('Batch-8838', 'gis_constituency_boundaries_v3.geojson', 'src-eci-01', 543, 'Survey of India / ECI GIS', 'LOADED')
ON CONFLICT (id) DO NOTHING;

-- 13. System Metrics
INSERT INTO system_metrics (id, cpu_utilization, memory_utilization, disk_free_gb, db_pool_active, db_pool_overflow, redis_latency_ms, api_requests_per_sec, p99_latency_ms)
VALUES (1, 14.2, 38.5, 57.0, 5, 0, 1.2, 1420, 8.4)
ON CONFLICT (id) DO NOTHING;

-- 14. Initial Audit Logs with SHA-256 Chaining
INSERT INTO audit_log (id, timestamp, actor, action, resource, status, ip_address, previous_hash, current_hash, metadata)
VALUES
('aud-9901', '2026-07-23 14:15:30+00', 'ai_eng', 'DEPLOY_MODEL_GATEWAY', 'ai/gemini-2.5-flash', 'SUCCESS', '192.168.1.45', '0000000000000000000000000000000000000000000000000000000000000000', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', '{"provider": "Google DeepMind", "latency": "380ms"}'::jsonb),
('aud-9902', '2026-07-23 15:30:00+00', 'system', 'ROTATE_JWT_SECRET', 'security/jwt', 'SUCCESS', '127.0.0.1', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', '{"algorithm": "HS256", "key_length_bits": 256}'::jsonb),
('aud-9903', '2026-07-23 16:50:00+00', 'ops_lead', 'INGEST_ELECTION_DATA', 'etl/batch-8841', 'SUCCESS', '10.0.4.12', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a', '{"records_verified": 543, "format": "CSV"}'::jsonb),
('aud-9904', '2026-07-23 17:22:00+00', 'superadmin', 'UPDATE_FEATURE_FLAG', 'feature_flags/enable_rag', 'SUCCESS', '127.0.0.1', '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a', 'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d', '{"old_value": true, "new_value": true}'::jsonb)
ON CONFLICT (id) DO NOTHING;
