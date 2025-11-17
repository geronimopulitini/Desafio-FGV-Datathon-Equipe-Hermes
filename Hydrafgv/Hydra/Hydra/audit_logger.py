from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


_AUDIT_LOGGER_NAME = "hydra.audit"
_AUDIT_LOG_PATH_ENV = "HYDRA_AUDIT_LOG_PATH"
_AUDIT_LOG_DIR_ENV = "HYDRA_AUDIT_LOG_DIR"
_AUDIT_RUN_ID_ENV = "HYDRA_RUN_ID"


def _default_audit_path() -> Path:
    """
    Caminho padrão do arquivo de auditoria.

    Pode ser sobrescrito via:
    - HYDRA_AUDIT_LOG_PATH (arquivo completo)
    - HYDRA_AUDIT_LOG_DIR (diretório; arquivo vira <dir>/audit.log)
    """
    explicit = os.getenv(_AUDIT_LOG_PATH_ENV)
    if explicit:
        return Path(explicit)
    base_dir = os.getenv(_AUDIT_LOG_DIR_ENV) or "logs"
    return Path(base_dir) / "audit.log"


def _ensure_logger() -> logging.Logger:
    logger = logging.getLogger(_AUDIT_LOGGER_NAME)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    path = _default_audit_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(path, encoding="utf-8")
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def _current_run_id() -> Optional[str]:
    value = os.getenv(_AUDIT_RUN_ID_ENV, "").strip()
    return value or None


def audit_event(event: str, **payload: Any) -> None:
    """
    Registra um evento de auditoria em formato JSON line (um JSON por linha).

    Campos padrão:
    - ts: timestamp UTC ISO
    - event: nome do evento (ex.: "api_call", "fallback")
    - run_id: opcional, herdado de HYDRA_RUN_ID
    - payload extra em **payload
    """
    logger = _ensure_logger()
    try:
        record: Dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "event": event,
        }
        run_id = _current_run_id()
        if run_id:
            record["run_id"] = run_id
        for key, value in payload.items():
            try:
                json.dumps(value)
                record[key] = value
            except Exception:
                record[key] = repr(value)
        logger.info(json.dumps(record, ensure_ascii=False))
    except Exception:
        # Nunca deixar a auditoria quebrar o fluxo principal
        return

