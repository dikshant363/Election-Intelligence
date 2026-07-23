# Roadmap

## 1. Vision Statement
To become the definitive, high-performance platform for real-time election intelligence, scaling to millions of users while maintaining enterprise-grade security and accuracy.

## 2. Current State (v1.0.0)
- **Status**: Stable
- Core platform delivered with 6 entities, search, AI RAG, realtime streams, and Flutter app.

## 3. Version Roadmap

| Version | Theme | Key Features |
|---------|-------|--------------|
| **v1.0.0** | Current | Core platform, 6 entities, search, AI RAG, realtime, Flutter app |
| **v1.1** | AI Intelligence | Enhanced RAG, multi-model support, trend detection, NLP query |
| **v1.2** | Developer Platform| Public REST API, SDKs, API keys, developer portal, webhooks |
| **v1.3** | Multi-tenant SaaS | Tenant isolation, billing, per-tenant config, self-service onboarding |
| **v1.4** | Gov Integrations | ECI data feeds, official connectors, audit compliance, certified provenance |
| **v2.0** | Next Generation | Real-time election night dashboard, live polling booth streams |

## 4. Complexity & Dependencies
- **v1.1**: Medium complexity. Depends on external LLM availability.
- **v1.2**: High complexity. Requires API gateway and quota management.
- **v1.3**: High complexity. Involves deep schema changes for multi-tenancy.
- **v1.4**: Medium complexity. Depends on government API access.

## 5. Contribution Opportunities
- Integrations with local data sources.
- Flutter UI enhancements.
- Additional AI evaluation models.

## 6. What is NOT on the Roadmap
- Social media platform integrations (outside scope).
- Automated trading based on election sentiment.

## 7. Proposing a Roadmap Item
Submit a PR proposing an RFC in the `docs/rfcs/` directory following the provided template.
