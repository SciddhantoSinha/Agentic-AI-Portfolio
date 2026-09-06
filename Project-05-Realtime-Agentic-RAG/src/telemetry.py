import time
from typing import Any, Dict, List


class TelemetryTracker:
    """
    Lightweight telemetry collector for the CRAG pipeline.

    Records pipeline events such as routing, retrieval, fallback,
    generation, and completion. The collected events can later be
    forwarded to observability platforms such as LangSmith or
    Arize Phoenix.
    """

    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self._start_time: float | None = None

    def start(self) -> None:
        """
        Start measuring pipeline execution time.
        """

        self._start_time = time.perf_counter()

    def record(
        self,
        event: str,
        metadata: Dict[str, Any] = None,
    ) -> None:
        """
        Record a pipeline event.

        Args:
            event: Name of the event.
            metadata: Optional event metadata.
        """

        if not event or not event.strip():
            raise ValueError(
                "event must not be empty."
            )

        self.events.append(
            {
                "event": event,
                "metadata": metadata or {},
                "timestamp": time.time(),
            }
        )

    def elapsed_ms(self) -> float:
        """
        Return elapsed pipeline time in milliseconds.
        """

        if self._start_time is None:
            return 0.0

        return (
            time.perf_counter()
            - self._start_time
        ) * 1000

    def finish(self) -> Dict[str, Any]:
        """
        Record pipeline completion and return a telemetry summary.
        """

        duration_ms = self.elapsed_ms()

        self.record(
            event="pipeline_complete",
            metadata={
                "duration_ms": round(
                    duration_ms,
                    2,
                ),
                "event_count": len(
                    self.events
                ),
            },
        )

        return {
            "duration_ms": round(
                duration_ms,
                2,
            ),
            "events": list(
                self.events
            ),
        }

    def clear(self) -> None:
        """
        Clear all recorded telemetry events.
        """

        self.events.clear()
        self._start_time = None
