# CONTROL CENTER OPERATIONAL PLAYBOOKS
## Enterprise Control Center — Version 1.0.0

---

## 1. Operational Procedures

### Flushing Platform Cache
When dataset changes require immediate cache invalidation across Redis and memory layers:
1. Navigate to **Enterprise Control Center** (`/admin`).
2. Trigger `POST /api/v1/admin/ops/flush-cache` or use Command Palette (`⌘ K` -> `Flush Cache`).
3. Verify cache stats reset to 0 in system health metrics.

### Search Index Reindexing
When FTS or vector embeddings require recalculation:
1. Open Command Palette (`⌘ K`).
2. Select **Reindex Search Engine (SAL)**.
3. Check `POST /api/v1/admin/ops/reindex` response status (`SUCCESS`).

### Feature Flag Emergency Toggles
To isolate an unstable feature without redeploying code:
1. Go to **Platform Feature Flags** in Enterprise Control Center.
2. Toggle switch for target flag (e.g. `enable_chaos_testing` or `enable_rag`).
3. API instantly respects the new boolean toggle state across worker nodes.
