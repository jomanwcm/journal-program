# constants.py
# -*- coding: utf-8 -*-
"""
App-wide constants and preset loading for the Trade Journal app.
Includes:
- COLUMNS / COLUMN_NAMES / COL_INDEX
- BUCKET_COLUMNS (the four label buckets)
- KINDS_BY_COL (index -> 'bull'/'bear'/'tr'/'bias')
- KIND_TO_COL (reverse mapping)
- Robust presets.json loader that works across machines

Discovery order for presets.json:
  0) Env var TRADE_JOURNAL_PRESETS_PATH
  1) Same folder as this file
  2) One level up (repo root when running from source)
  3) Walk up from current working directory
  4) Package data (if bundled)
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple, Dict
from collections import OrderedDict
import json
import os

APP_NAME: str = "Trade Journal"

# --------------------
# Columns definition
# --------------------
# Must match the tksheet layout in journal_app.py
COLUMNS = OrderedDict([
    ("Bar",  {"width": 60}),
    ("Bull", {"width": 250}),
    ("Bear", {"width": 250}),
    ("TR",   {"width": 250}),
    ("Bias", {"width": 200}),
])

COLUMN_NAMES: List[str] = list(COLUMNS.keys())
# name -> index mapping
COL_INDEX: Dict[str, int] = {name: i for i, name in enumerate(COLUMN_NAMES)}

# The four “bucket” columns that hold labels/presets
BUCKET_COLUMNS: List[str] = ["Bull", "Bear", "TR", "Bias"]

# Kinds mapping used by button panels and journal_app logic
# index -> kind
KINDS_BY_COL: Dict[int, str] = {
    COL_INDEX["Bull"]: "bull",
    COL_INDEX["Bear"]: "bear",
    COL_INDEX["TR"]:   "tr",
    COL_INDEX["Bias"]: "bias",
}
# kind -> index (reverse lookup)
KIND_TO_COL: Dict[str, int] = {v: k for k, v in KINDS_BY_COL.items()}

# --------------------
# Bars / Rows ordering
# --------------------
BAR_ORDER: List[str] = ["RTH", "ETH"] + [str(i) for i in range(1, 82)]

# ---------------------------------
# Built-in defaults (safe fallback)
# ---------------------------------
BULL_POINTS_DEFAULT: List[str] = [
    "Strong bull close",
    "Two-legged pullback bull (H2)",
    "Decent bull bar()",
    "Bull BO + follow-through",
    "Micro DB -> bull scalp",
    "Bull TTR -> upside BO test",
    "Test of MA holding as support",
    "Buy the close context",
]

BEAR_POINTS_DEFAULT: List[str] = [
    "Strong bear close",
    "Two-legged pullback bear (L2)",
    "Decent bear bar()",
    "Bear BO + follow-through",
    "Micro DT -> bear scalp",
    "Bear TTR -> downside BO test",
    "Test of MA holding as resistance",
    "Sell the close context",
]

TR_POINTS_DEFAULT: List[str] = [
    "Trading range day",
    "Range high test / sellers above",
    "Range low test / buyers below",
    "TTR developing",
    "Failed BO -> reversal risk",
    "Mid-range magnet",
    "Wait for a strong BO",
]

BIAS_POINTS_DEFAULT: List[str] = [
    "Bull bias",
    "Bear bias",
    "Sideways / TR bias",
    "Buy climax risk",
    "Sell climax risk",
    "Opening reversal risk",
]

# -------------------------------------------------------
# Robust presets.json discovery
# -------------------------------------------------------
PRESETS_ORIGIN: str = "built-in defaults"

def _normalize_list(value, fallback: List[str]) -> List[str]:
    if not isinstance(value, list):
        return fallback
    out = [str(x).strip() for x in value if str(x).strip()]
    return out or fallback

def _candidate_paths_for_presets() -> List[Path]:
    candidates: List[Path] = []

    # 0) ENV override
    env_path = os.environ.get("TRADE_JOURNAL_PRESETS_PATH")
    if env_path:
        candidates.append(Path(env_path).expanduser())

    # 1) Same folder as this file
    here = Path(__file__).resolve().parent
    candidates.append(here / "presets.json")

    # 2) One level up (repo root when running from source)
    candidates.append(here.parent / "presets.json")

    # 3) Walk up from current working directory
    try:
        cwd = Path.cwd().resolve()
        for p in [cwd, *cwd.parents]:
            candidates.append(p / "presets.json")
    except Exception:
        pass

    # 4) Package data (if bundled)
    try:
        from importlib.resources import files as _res_files
        pkg_file = _res_files(__package__).joinpath("presets.json")
        try:
            pf = Path(str(pkg_file))
            if pf.is_file():
                candidates.append(pf)
        except Exception:
            pass
    except Exception:
        pass

    # De-dup while preserving order
    seen = set()
    unique: List[Path] = []
    for c in candidates:
        try:
            key = c.resolve()
        except Exception:
            key = c
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique

def _load_project_presets() -> Tuple[List[str], List[str], List[str], List[str], str]:
    global PRESETS_ORIGIN
    for path in _candidate_paths_for_presets():
        try:
            if path and path.is_file():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                bull = _normalize_list(data.get("bull_points"), BULL_POINTS_DEFAULT)
                bear = _normalize_list(data.get("bear_points"), BEAR_POINTS_DEFAULT)
                tr   = _normalize_list(data.get("tr_points"),   TR_POINTS_DEFAULT)
                bias = _normalize_list(data.get("bias_points"), BIAS_POINTS_DEFAULT)
                PRESETS_ORIGIN = str(path)
                print(f"[{APP_NAME}] Loaded presets from: {path}")
                return bull, bear, tr, bias, PRESETS_ORIGIN
        except Exception:
            continue

    PRESETS_ORIGIN = "built-in defaults"
    print(f"[{APP_NAME}] Using built-in preset defaults (presets.json not found).")
    return (
        BULL_POINTS_DEFAULT,
        BEAR_POINTS_DEFAULT,
        TR_POINTS_DEFAULT,
        BIAS_POINTS_DEFAULT,
        PRESETS_ORIGIN,
    )

# Load presets at import time
BULL_POINTS, BEAR_POINTS, TR_POINTS, BIAS_POINTS, _ = _load_project_presets()

__all__ = [
    "APP_NAME",
    "BAR_ORDER",
    "COLUMNS",
    "COLUMN_NAMES",
    "COL_INDEX",
    "BUCKET_COLUMNS",
    "KINDS_BY_COL",
    "KIND_TO_COL",
    "BULL_POINTS_DEFAULT",
    "BEAR_POINTS_DEFAULT",
    "TR_POINTS_DEFAULT",
    "BIAS_POINTS_DEFAULT",
    "BULL_POINTS",
    "BEAR_POINTS",
    "TR_POINTS",
    "BIAS_POINTS",
    "PRESETS_ORIGIN",
]
