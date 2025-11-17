from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict

CONFIG_PATH = Path(__file__).resolve().parent / "config" / "conviction_presets.json"


@dataclass(frozen=True)
class CategoryParams:
    sentiment_weight: float
    cz_weight: float
    sensitivity: float


@dataclass(frozen=True)
class ConvictionPreset:
    name: str
    tau: float
    global_params: CategoryParams
    categories: Dict[str, CategoryParams]
    asset_categories: Dict[str, str]

    def params_for_asset(self, ticker: str) -> CategoryParams:
        cat = self.asset_categories.get(ticker.upper())
        if cat and cat in self.categories:
            return self.categories[cat]
        return self.global_params

    def sensitivity_map(self, assets) -> Dict[str, float]:
        return {
            asset: self.params_for_asset(asset).sensitivity for asset in assets
        }


def _load_raw_config(path: Path = CONFIG_PATH) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Conviction presets config não encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=16)
def load_conviction_preset(name: str, path: Path | None = None) -> ConvictionPreset:
    cfg = _load_raw_config(path or CONFIG_PATH)
    presets = cfg.get("presets") or {}
    preset_data = presets.get(name) or presets.get("moderado")
    if preset_data is None:
        raise ValueError(f"Preset {name} não encontrado em config.")

    def _parse_category(block: dict | None, fallback: CategoryParams) -> CategoryParams:
        if not block:
            return fallback
        sw = float(block.get("sentiment_weight", fallback.sentiment_weight))
        cz = float(block.get("cz_weight", fallback.cz_weight))
        sen = float(block.get("sensitivity", fallback.sensitivity))
        return CategoryParams(sw, cz, sen)

    global_params = _parse_category(preset_data.get("global"), CategoryParams(0.5, 0.5, 0.05))
    categories_cfg = preset_data.get("categories") or {}
    categories: Dict[str, CategoryParams] = {}
    for key, block in categories_cfg.items():
        categories[key] = _parse_category(block, global_params)

    assets = {k.upper(): str(v) for k, v in (cfg.get("assets") or {}).items()}
    return ConvictionPreset(
        name=name,
        tau=float(preset_data.get("tau", 0.05)),
        global_params=global_params,
        categories=categories,
        asset_categories=assets,
    )

