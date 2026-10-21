'use client';

import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  ShieldAlert,
  RefreshCw,
  Download,
  AlertTriangle,
  CheckCircle2,
  X,
  FileCode,
  Copy,
  Check,
  Database,
  Lock,
} from 'lucide-react';
import {
  runAutomatedChecksumScan,
  simulateStorageTamper,
  restoreStorageIntegrity,
  exportChecksumReportCSV,
  getTamperedDatasetId,
} from '@/lib/checksumValidation';
import type { ChecksumValidationReport } from '@/lib/types';
import { speakVoiceOver, announceCriticalAlert, announceOperation } from '@/lib/voiceOver';

interface StorageChecksumModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLogAudit?: (action: string, resource: string, status: string) => void;
}

export function StorageChecksumModal({
  isOpen,
  onClose,
  onLogAudit,
}: StorageChecksumModalProps) {
  const [report, setReport] = useState<ChecksumValidationReport | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [copiedHash, setCopiedHash] = useState<string | null>(null);

  const handleRunScan = async (announce: boolean = true) => {
    setIsScanning(true);
    if (announce) {
      announceOperation('Initiating automated checksum verification across all electoral storage layers.');
    }

    // Small delay to provide natural scanning animation
    await new Promise((resolve) => setTimeout(resolve, 400));
    const result = await runAutomatedChecksumScan();
    setReport(result);
    setIsScanning(false);

    if (result.overallStatus === 'SECURE') {
      if (announce) {
        speakVoiceOver(
          `Checksum validation complete: ${result.verifiedCount} of ${result.totalDatasetsScanned} electoral datasets verified with zero bit-rot or corruption detected.`,
          { priority: 'normal' }
        );
      }
      onLogAudit?.(
        'CHECKSUM_VERIFY_PASSED',
        `MerkleRoot:${result.merkleRootHash.substring(0, 12)}`,
        'VERIFIED'
      );
    } else {
      announceCriticalAlert(
        `Critical Alert: Storage checksum mismatch detected in ${result.anomaliesCount} dataset. Potential unauthorized modification or storage corruption flagged.`,
        'critical'
      );
      onLogAudit?.(
        'CHECKSUM_TAMPER_ALERT',
        `MerkleRoot:${result.merkleRootHash.substring(0, 12)}`,
        'ANOMALY_DETECTED'
      );
    }
  };

  useEffect(() => {
    if (isOpen && !report) {
      handleRunScan(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSimulateTamper = async (datasetId: string) => {
    simulateStorageTamper(datasetId);
    await handleRunScan(true);
  };

  const handleRestoreIntegrity = async () => {
    restoreStorageIntegrity();
    announceOperation('Cryptographic storage baseline restored. Re-running checksum verification.');
    await handleRunScan(true);
  };

  const handleCopyHash = (hash: string) => {
    navigator.clipboard.writeText(hash);
    setCopiedHash(hash);
    setTimeout(() => setCopiedHash(null), 2000);
  };

  const hasAnomalies = report ? report.anomaliesCount > 0 : false;
  const tamperedId = getTamperedDatasetId();

  return (
    <div className="fixed inset-0 z-50 bg-black/45 dark:bg-black/70 backdrop-blur-md flex items-center justify-center p-3 sm:p-5">
      <div className="bg-white/95 dark:bg-[#1c1c1e]/95 backdrop-blur-3xl border border-black/[0.08] dark:border-white/[0.12] rounded-3xl p-5 sm:p-7 shadow-2xl max-w-4xl w-full max-h-[92vh] flex flex-col justify-between animate-in fade-in zoom-in-95 duration-150 transition-colors">
        {/* Modal Header */}
        <div className="flex items-start justify-between pb-4 border-b border-black/[0.06] dark:border-white/[0.08]">
          <div className="flex items-center gap-3">
            <div
              className={`w-10 h-10 rounded-2xl flex items-center justify-center shadow-xs transition-colors ${
                hasAnomalies
                  ? 'bg-[#ff3b30]/15 text-[#ff3b30]'
                  : 'bg-[#34c759]/15 text-[#34c759]'
              }`}
            >
              {hasAnomalies ? (
                <ShieldAlert className="w-5 h-5 animate-pulse" />
              ) : (
                <ShieldCheck className="w-5 h-5" />
              )}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-[17px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">
                  Automated Storage Checksum Validation
                </h3>
                <span
                  className={`text-[11px] font-medium px-2 py-0.5 rounded-full ${
                    hasAnomalies
                      ? 'bg-[#ff3b30]/10 text-[#ff3b30]'
                      : 'bg-[#34c759]/10 text-[#34c759]'
                  }`}
                >
                  {hasAnomalies ? 'ANOMALY DETECTED' : 'BIT-FOR-BIT SECURE'}
                </span>
              </div>
              <p className="text-[12px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
                Bitwise SHA-256 cryptographic verification of persistent electoral storage layers
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="p-1.5 rounded-xl text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/[0.04] dark:hover:bg-white/[0.08] transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Verification Summary KPIs Strip */}
        {report && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 my-4">
            <div className="p-3 rounded-2xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
              <div className="text-[11px] text-[#86868b] font-medium">Validation Status</div>
              <div
                className={`text-lg font-bold mt-0.5 flex items-center gap-1.5 ${
                  hasAnomalies ? 'text-[#ff3b30]' : 'text-[#34c759]'
                }`}
              >
                {hasAnomalies ? 'Tamper Detected' : 'All Verified'}
              </div>
              <div className="text-[10px] text-[#86868b] mt-0.5">
                {report.verifiedCount} of {report.totalDatasetsScanned} datasets matched
              </div>
            </div>

            <div className="p-3 rounded-2xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
              <div className="text-[11px] text-[#86868b] font-medium">Merkle Root Hash</div>
              <div className="font-mono text-[12px] font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] mt-1 flex items-center gap-1.5 truncate">
                <span>{report.merkleRootHash.substring(0, 14)}...</span>
                <button
                  type="button"
                  onClick={() => handleCopyHash(report.merkleRootHash)}
                  className="p-1 hover:bg-black/[0.05] dark:hover:bg-white/[0.1] rounded transition"
                  title="Copy full Merkle Root"
                >
                  {copiedHash === report.merkleRootHash ? (
                    <Check className="w-3 h-3 text-[#34c759]" />
                  ) : (
                    <Copy className="w-3 h-3 text-[#86868b]" />
                  )}
                </button>
              </div>
              <div className="text-[10px] text-[#86868b] mt-0.5">SHA-256 Composite Root</div>
            </div>

            <div className="p-3 rounded-2xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
              <div className="text-[11px] text-[#86868b] font-medium">Scan Duration</div>
              <div className="text-lg font-bold text-[#1d1d1f] dark:text-[#f5f5f7] mt-0.5">
                {report.durationMs} ms
              </div>
              <div className="text-[10px] text-[#86868b] mt-0.5">High-throughput I/O scan</div>
            </div>

            <div className="p-3 rounded-2xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.04]">
              <div className="text-[11px] text-[#86868b] font-medium">Corrupted Datasets</div>
              <div
                className={`text-lg font-bold mt-0.5 ${
                  hasAnomalies ? 'text-[#ff3b30]' : 'text-[#34c759]'
                }`}
              >
                {report.anomaliesCount} Anomaly
              </div>
              <div className="text-[10px] text-[#86868b] mt-0.5">
                {hasAnomalies ? 'Bit-flip detected' : 'Zero unauthorized edits'}
              </div>
            </div>
          </div>
        )}

        {/* Anomaly Alert Callout Banner if detected */}
        {hasAnomalies && (
          <div className="mb-3 p-3.5 rounded-2xl bg-[#ff3b30]/10 border border-[#ff3b30]/25 text-[12px] flex items-start gap-3 animate-in fade-in slide-in-from-top-1">
            <AlertTriangle className="w-4 h-4 text-[#ff3b30] shrink-0 mt-0.5" />
            <div className="flex-1">
              <div className="font-semibold text-[#ff3b30]">
                Security Alert: Storage Layer Integrity Checksum Failure
              </div>
              <p className="text-[#1d1d1f] dark:text-[#f5f5f7] mt-0.5 opacity-90 leading-relaxed">
                The computed SHA-256 hash does not match the baseline genesis signature for{' '}
                <strong className="underline">
                  {report?.records.find((r) => r.status === 'TAMPERED')?.datasetName}
                </strong>
                . Possible storage bit corruption, hardware fault, or unauthorized direct modification.
              </p>
            </div>
            <button
              type="button"
              onClick={handleRestoreIntegrity}
              className="px-3 py-1.5 rounded-xl bg-[#34c759] hover:bg-[#30be53] text-white text-[11px] font-semibold transition active:scale-95 shadow-sm cursor-pointer shrink-0"
            >
              Restore &amp; Re-verify
            </button>
          </div>
        )}

        {/* Dataset Checksum Table */}
        <div className="flex-1 overflow-y-auto max-h-72 border border-black/[0.06] dark:border-white/[0.08] rounded-2xl">
          <table className="w-full text-left text-[12px]">
            <thead className="sticky top-0 z-10 bg-[#f5f5f7] dark:bg-[#252528] text-[#86868b] dark:text-[#a1a1a6] text-[11px] uppercase tracking-wider border-b border-black/[0.06] dark:border-white/[0.08]">
              <tr>
                <th className="py-2.5 px-3 font-semibold">Electoral Dataset</th>
                <th className="py-2.5 px-3 font-semibold">Storage Layer Path</th>
                <th className="py-2.5 px-3 font-semibold">Expected Genesis Hash</th>
                <th className="py-2.5 px-3 font-semibold">Computed Hash</th>
                <th className="py-2.5 px-3 font-semibold text-center">Status</th>
                <th className="py-2.5 px-3 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-black/[0.03] dark:divide-white/[0.03]">
              {report?.records.map((r) => {
                const isTampered = r.status === 'TAMPERED';
                return (
                  <tr
                    key={r.id}
                    className={`transition-colors ${
                      isTampered
                        ? 'bg-[#ff3b30]/[0.06] dark:bg-[#ff3b30]/[0.08]'
                        : 'hover:bg-black/[0.015] dark:hover:bg-white/[0.02]'
                    }`}
                  >
                    <td className="py-3 px-3">
                      <div className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                        {r.datasetName}
                      </div>
                      <div className="text-[11px] text-[#86868b]">
                        {r.recordCount.toLocaleString()} rows · {(r.sizeBytes / 1024 / 1024).toFixed(2)} MB
                      </div>
                    </td>

                    <td className="py-3 px-3 font-mono text-[11px] text-[#86868b] truncate max-w-[160px]">
                      {r.storageLayerPath}
                    </td>

                    <td className="py-3 px-3 font-mono text-[11px] text-[#86868b]">
                      <span title={r.expectedChecksum}>
                        {r.expectedChecksum.substring(0, 10)}...{r.expectedChecksum.substring(58)}
                      </span>
                    </td>

                    <td className="py-3 px-3 font-mono text-[11px]">
                      <span
                        className={
                          isTampered
                            ? 'text-[#ff3b30] font-bold bg-[#ff3b30]/10 px-1 py-0.5 rounded'
                            : 'text-[#34c759] font-medium'
                        }
                        title={r.computedChecksum}
                      >
                        {r.computedChecksum.substring(0, 10)}...{r.computedChecksum.substring(58)}
                      </span>
                    </td>

                    <td className="py-3 px-3 text-center whitespace-nowrap">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold ${
                          isTampered
                            ? 'bg-[#ff3b30]/15 text-[#ff3b30]'
                            : 'bg-[#34c759]/15 text-[#34c759]'
                        }`}
                      >
                        {isTampered ? (
                          <>
                            <AlertTriangle className="w-3 h-3" />
                            MISMATCH
                          </>
                        ) : (
                          <>
                            <Check className="w-3 h-3" />
                            MATCHED
                          </>
                        )}
                      </span>
                    </td>

                    <td className="py-3 px-3 text-right whitespace-nowrap">
                      {isTampered ? (
                        <button
                          type="button"
                          onClick={handleRestoreIntegrity}
                          className="text-[11px] font-semibold text-[#0071e3] hover:underline cursor-pointer"
                        >
                          Heal Record
                        </button>
                      ) : (
                        <button
                          type="button"
                          onClick={() => handleSimulateTamper(r.id)}
                          className="text-[11px] text-[#86868b] hover:text-[#ff3b30] transition cursor-pointer"
                          title="Simulate unauthorized bit-flip modification in this storage dataset"
                        >
                          Simulate Tamper
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Modal Footer Controls */}
        <div className="pt-4 mt-3 border-t border-black/[0.06] dark:border-white/[0.08] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2 text-[11px] text-[#86868b]">
            <Lock className="w-3.5 h-3.5 text-[#34c759]" />
            <span>FIPS 180-4 Secure Hash Standard · Storage Block SHA-256 Engine</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => report && exportChecksumReportCSV(report)}
              disabled={!report}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] text-[12px] font-medium transition cursor-pointer active:scale-95"
            >
              <Download className="w-3.5 h-3.5 text-[#0071e3] dark:text-[#2997ff]" />
              <span>Export Audit CSV</span>
            </button>

            <button
              type="button"
              onClick={() => handleRunScan(true)}
              disabled={isScanning}
              className="flex items-center gap-1.5 px-4 py-1.5 rounded-xl bg-[#0071e3] hover:bg-[#0077ed] text-white text-[12px] font-medium transition active:scale-95 shadow-sm cursor-pointer disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isScanning ? 'animate-spin' : ''}`} />
              <span>{isScanning ? 'Verifying Hashes...' : 'Re-verify All Checksums'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
