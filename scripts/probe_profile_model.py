#!/usr/bin/env python3
"""Fail early when the configured profile model is unavailable from this runner."""

import json
import logging
import os
import time
from contextlib import suppress

from iot_profile_builder.generator.profile_generator import ProfileGenerator
from iot_profile_builder.models import ScanConfig


def main() -> int:
    """Emit only one bounded diagnostic JSON object, never provider response text."""
    logging.disable(logging.CRITICAL)
    started = time.monotonic()
    model = os.environ.get("PROFILE_LLM_MODEL", "").strip()
    generator = None
    try:
        if not model or "://" in model or not os.environ.get("ANTHROPIC_BASE_URL", "").strip():
            raise ValueError("Explicit model and endpoint are required")
        generator = ProfileGenerator(
            ScanConfig(username="model-preflight", llm_model=model, strict_scan=True)
        )
        result = generator.probe()
    except Exception:
        result = {
            "mode": "model_preflight",
            "status": "failed",
            "error": "configuration_error",
            "duration_seconds": round(time.monotonic() - started, 3),
        }
    finally:
        if generator is not None:
            with suppress(Exception):
                generator.client.close()
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
