"""Minimal YAML configuration loader for the project.

This module exposes two helpers:

``load_config`` loads the entire configuration dictionary, parsing the
``config.yaml`` file. ``get_config_value`` provides convenient access to
individual settings with optional overrides so tests or callers can supply
temporary configuration values.
"""
from __future__ import annotations

from typing import Any, Dict
import copy
import os


def load_config(path: str | None = None) -> Dict[str, Any]:
    """Parse ``config.yaml`` and return its contents as a dictionary."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "config.yaml")

    config: Dict[str, Any] = {}
    stack = [config]
    indents = [0]
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip())
            while indent < indents[-1]:
                stack.pop()
                indents.pop()
            key, _, rest = line.lstrip().partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest == "":
                child: Dict[str, Any] = {}
                stack[-1][key] = child
                stack.append(child)
                indents.append(indent + 2)
            else:
                value: Any = rest
                try:
                    numeric = float(value)
                    if numeric.is_integer() and not any(c in value for c in [".", "e", "E"]):
                        value = int(numeric)
                    else:
                        value = numeric
                except ValueError:
                    if value.isdigit():
                        value = int(value)
                stack[-1][key] = value
    return config


_CONFIG = load_config()


def get_config_value(
    path: str,
    default: Any | None = None,
    overrides: Dict[str, Any] | None = None,
) -> Any:
    """Return a configuration value.

    ``path`` is a dot-delimited string (e.g. ``"teacher.difficulty"``). If
    ``overrides`` are provided they take precedence over the loaded config
    without mutating the global configuration.
    """

    def _lookup(cfg: Dict[str, Any], parts: list[str]) -> Any | None:
        cur: Any = cfg
        for part in parts:
            if not isinstance(cur, dict) or part not in cur:
                return None
            cur = cur[part]
        return cur

    parts = path.split(".")

    # Environment variable override. "teacher.alert_email" becomes
    # ``TEACHER_ALERT_EMAIL``. If set, it takes precedence over the
    # loaded configuration and any ``overrides`` mapping.
    env_name = "_".join(part.upper() for part in parts)
    env_val = os.environ.get(env_name)
    if env_val is not None:
        return env_val
    if overrides:
        merged = copy.deepcopy(_CONFIG)

        def _merge(dst: Dict[str, Any], src: Dict[str, Any]) -> None:
            for k, v in src.items():
                if isinstance(v, dict) and isinstance(dst.get(k), dict):
                    _merge(dst[k], v)
                else:
                    dst[k] = v

        _merge(merged, overrides)
        value = _lookup(merged, parts)
        if value is not None:
            return value

    value = _lookup(_CONFIG, parts)
    return value if value is not None else default
