# Election Domain Knowledge Guide

This guide introduces engineers to the core concepts of the Indian electoral system necessary to understand the Election Intelligence Platform's domain model.

## 1. Indian Election System Overview

- **Constitutional Framework**: Governed by Articles 324-329 of the Constitution of India, which mandate free and fair elections.
- **Election Commission of India (ECI)**: The autonomous constitutional authority responsible for administering all electoral processes in India.
- **Types of Elections**:
  - *Lok Sabha*: General elections for the lower house of Parliament (Prime Minister is chosen from the majority party).
  - *Rajya Sabha*: Indirect elections for the upper house.
  - *State Assembly (Vidhan Sabha)*: Elections for state legislative assemblies (Chief Minister chosen).
  - *State Council (Vidhan Parishad)*: Indirect elections in states with a bicameral legislature.
  - *Local Body*: Municipal and Panchayat elections.
  - *By-elections*: Held to fill mid-term vacancies.

## 2. Key Domain Entities

- **Election**: A specific electoral event defined by type, year, phase, schedule, and formal notification date.
- **Constituency**: An electoral district. There are 543 Lok Sabha constituencies and 4120 State Assembly constituencies total. Boundaries are defined by *delimitation*. Certain seats are *reserved* for Scheduled Castes (SC) and Scheduled Tribes (ST).
- **Candidate**: An individual contesting an election. They must file a nomination and submit affidavits detailing criminal records, assets, and liabilities.
- **Party**: Political organizations categorized as National Parties, State Parties, or Registered Unrecognised Parties. They are assigned specific *symbols*.
- **PollingBooth**: A specific physical location where voters cast their ballots. Data includes assigned voters and booth-level turnout.
- **Result**: The outcome of an election in a constituency. Includes the winner, runner-up, win margin, EVM vote count, postal ballot count, total valid votes, and NOTA votes.

## 3. Key Terminology

- **FPTP (First Past the Post)**: The electoral system where the candidate with the highest number of votes wins, regardless of whether they secure an absolute majority.
- **EVM (Electronic Voting Machine)**: The electronic devices used to record votes.
- **VVPAT (Voter Verified Paper Audit Trail)**: A printer attached to the EVM that generates a paper slip verifying the voter's choice.
- **MCC (Model Code of Conduct)**: Guidelines issued by the ECI regulating the conduct of political parties and candidates during elections.
- **NOTA (None of the Above)**: A ballot option allowing voters to officially reject all candidates.
- **Nomination & Affidavit (Form 26)**: The legal documentation filed by candidates declaring their financial assets, criminal history, and educational background.
- **Winnability Analysis**: The statistical assessment of a candidate's likelihood of winning based on historical data and demographics.

## 4. Data Sources

- **Election Commission of India (eci.gov.in)**: Primary source for results, schedules, and voter turnout.
- **MyNeta.info / ADR (Association for Democratic Reforms)**: Primary sources for parsed candidate affidavits (assets, criminal cases).
- **VoterHelpline**: Official app/data for voter registration statistics.

## 5. Data Quality Challenges

- **Name Transliteration**: Candidate names often appear differently across sources due to transliteration between English, Hindi, and regional scripts.
- **Party Name Variations & Alliances**: Parties frequently change names, split, or form pre/post-poll alliances, complicating historical tracking.
- **Delimitation**: Constituency boundaries and names change periodically (e.g., the 2008 delimitation), making long-term historical comparisons difficult.
- **Multi-Phase Elections**: General elections occur over several weeks in multiple phases, requiring complex temporal data modeling.

## 6. Domain to Code Mapping

| Domain Concept | Python Entity (Backend) | Database Table (PostgreSQL) | Primary API Endpoint |
|---|---|---|---|
| Election | `ElectionModel` | `elections` | `/api/v1/elections` |
| Constituency | `ConstituencyModel` | `constituencies` | `/api/v1/constituencies` |
| Candidate | `CandidateModel` | `candidates` | `/api/v1/candidates` |
| Party | `PartyModel` | `parties` | `/api/v1/parties` |
| Polling Booth | `PollingBoothModel` | `polling_booths` | `/api/v1/booths` |
| Result | `ResultModel` | `results` | `/api/v1/results` |

## 7. Common Queries and Analytics

- **Win Margin Analysis**: Calculating the difference in votes between the winner and the runner-up to identify highly competitive "swing" seats.
- **Voter Turnout Analysis**: Tracking the percentage of eligible voters who cast ballots, broken down by demographics or region.
- **Candidate Asset Growth Analysis**: Comparing a returning candidate's financial assets declared in the current election against previous affidavits.
- **Party Performance Over Elections**: Tracking vote share and seat share changes for a party across multiple election cycles.

## 8. Glossary of Terms

*(A selection of common terms. See the full glossary in the developer wiki.)*

- **By-election**: An election held to fill a political office that has become vacant between general elections.
- **Delimitation**: The act of redrawing the boundaries of assembly or Lok Sabha constituencies to reflect changes in population.
- **Electoral Roll**: The official list of registered voters for a constituency.
- **Incumbent**: The current holder of a political office.
- **Manifesto**: A published declaration of the intentions, motives, or views of a political party.
- **Postal Ballot**: Votes cast by mail, typically utilized by service personnel and election officials on duty.
- **Reserved Constituency**: Seats where only candidates from Scheduled Castes (SC) or Scheduled Tribes (ST) can contest.
- **Swing**: The percentage of voters switching their support from one party to another.
