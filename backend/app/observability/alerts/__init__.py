"""Alerting framework with configurable rules, thresholds, and notification adapters."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime

from app.observability.schemas import AlertRuleSchema

logger = logging.getLogger("app.observability.alerts")


@dataclass
class AlertRule:
    """Configurable alert rule condition."""

    name: str
    threshold: float
    severity: str = "warning"
    comparison: str = ">"  # >, <, >=, <=
    is_firing: bool = False
    triggered_at: str | None = None

    def evaluate(self, value: float) -> bool:
        firing = False
        if (
            (self.comparison == ">" and value > self.threshold)
            or (self.comparison == ">=" and value >= self.threshold)
            or (self.comparison == "<" and value < self.threshold)
        ):
            firing = True

        if firing and not self.is_firing:
            self.is_firing = True
            self.triggered_at = datetime.now(UTC).isoformat()
            logger.warning(
                "ALERT FIRING [%s]: %s value %.2f %s threshold %.2f",
                self.severity,
                self.name,
                value,
                self.comparison,
                self.threshold,
            )
        elif not firing and self.is_firing:
            self.is_firing = False
            self.triggered_at = None
            logger.info("ALERT RESOLVED: %s", self.name)

        return self.is_firing


class AlertManager:
    """Evaluates rules across latency, worker failures, DLQ growth, and provider issues."""

    def __init__(self) -> None:
        self._rules: dict[str, AlertRule] = {
            "high_http_latency": AlertRule("high_http_latency", threshold=1000.0, severity="warning"),
            "high_worker_failures": AlertRule("high_worker_failures", threshold=5.0, severity="critical"),
            "dlq_growth": AlertRule("dlq_growth", threshold=10.0, severity="critical"),
            "ai_provider_error_rate": AlertRule("ai_provider_error_rate", threshold=0.1, severity="critical"),
        }

    def evaluate_metric(self, rule_name: str, value: float) -> AlertRuleSchema | None:
        rule = self._rules.get(rule_name)
        if not rule:
            return None

        is_firing = rule.evaluate(value)
        return AlertRuleSchema(
            rule_name=rule.name,
            severity=rule.severity,
            is_firing=is_firing,
            threshold=rule.threshold,
            current_value=value,
            triggered_at=rule.triggered_at,
        )

    def list_alerts(self) -> list[AlertRuleSchema]:
        return [
            AlertRuleSchema(
                rule_name=r.name,
                severity=r.severity,
                is_firing=r.is_firing,
                threshold=r.threshold,
                current_value=0.0,
                triggered_at=r.triggered_at,
            )
            for r in self._rules.values()
        ]


# Singleton alert manager
global_alert_manager = AlertManager()
