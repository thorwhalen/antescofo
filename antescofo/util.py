"""
Configuration management and utilities for Antescofo.

Handles user config files in ~/.config/antescofo and provides path resolution.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# User configuration directory
CONFIG_DIR = Path.home() / ".config" / "antescofo"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Default configuration values
_DEFAULT_CONFIG = {
    "antescofo_send_port": 5678,
    "python_receive_port": 9999,
    "pd_listen_port": 10000,  # Port where PD synth listens for OSC
    "pd_patch_path": None,  # User should set this
    "antescofo_external_path": "/Applications/Pd-0.56-2.app/Contents/Resources/extra/",
    "default_score_dir": str(Path.home() / "Music" / "antescofo_scores"),
    "enable_logging": True,
    "log_level": "INFO",
}

# Cached config
_cached_config: Optional[Dict[str, Any]] = None


def ensure_config_dir() -> Path:
    """
    Ensure the configuration directory exists.

    Returns:
        Path to the configuration directory
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR


def _get_default_pd_patch_path() -> str:
    """Find the default PD patch path in the package."""
    # Try to find the pd_synth_patch.pd in the package
    package_dir = Path(__file__).parent
    pd_patch = package_dir / "pd_synth_patch.pd"
    if pd_patch.exists():
        return str(pd_patch)
    return ""


def init_config(force: bool = False) -> Path:
    """
    Initialize user configuration with defaults.

    Creates ~/.config/antescofo/config.json with default settings.

    Args:
        force: If True, overwrite existing config

    Returns:
        Path to the config file
    """
    ensure_config_dir()

    if CONFIG_FILE.exists() and not force:
        logger.info(f"Config already exists at {CONFIG_FILE}")
        return CONFIG_FILE

    # Create default config with user-specific paths
    config = _DEFAULT_CONFIG.copy()
    config["pd_patch_path"] = _get_default_pd_patch_path()

    # Save config
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

    logger.info(f"Created config file at {CONFIG_FILE}")
    return CONFIG_FILE


def load_config(reload: bool = False) -> Dict[str, Any]:
    """
    Load user configuration.

    Args:
        reload: If True, bypass cache and reload from disk

    Returns:
        Configuration dictionary
    """
    global _cached_config

    if _cached_config is not None and not reload:
        return _cached_config

    # Ensure config exists
    if not CONFIG_FILE.exists():
        init_config()

    # Load config
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

        # Merge with defaults (in case new keys were added)
        merged = _DEFAULT_CONFIG.copy()
        merged.update(config)

        _cached_config = merged
        return merged

    except Exception as e:
        logger.warning(f"Failed to load config: {e}. Using defaults.")
        return _DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]):
    """
    Save configuration to file.

    Args:
        config: Configuration dictionary to save
    """
    global _cached_config
    ensure_config_dir()

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

    _cached_config = config
    logger.info(f"Saved config to {CONFIG_FILE}")


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a specific configuration value.

    Args:
        key: Configuration key
        default: Default value if key not found

    Returns:
        Configuration value
    """
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any):
    """
    Set a specific configuration value and save.

    Args:
        key: Configuration key
        value: Value to set
    """
    config = load_config()
    config[key] = value
    save_config(config)


def resolve_score_path(score_name: str) -> Path:
    """
    Resolve a score file path.

    If score_name is relative, looks in the default score directory.
    If absolute, uses as-is.

    Args:
        score_name: Score filename or path

    Returns:
        Resolved absolute path
    """
    score_path = Path(score_name)

    if score_path.is_absolute():
        return score_path

    # Try current directory first
    if score_path.exists():
        return score_path.resolve()

    # Try default score directory
    default_dir = Path(get_config_value("default_score_dir", "."))
    default_path = default_dir / score_name

    if default_path.exists():
        return default_path

    # Return current directory version (may not exist yet)
    return score_path.resolve()


def get_pd_patch_path() -> Optional[Path]:
    """
    Get the path to the PD synth patch.

    Returns:
        Path to pd_synth_patch.pd or None if not configured
    """
    path = get_config_value("pd_patch_path")
    if path:
        return Path(path)
    return None


def print_config():
    """Print the current configuration."""
    config = load_config()
    print("\n=== Antescofo Configuration ===")
    print(f"Config file: {CONFIG_FILE}")
    print("\nSettings:")
    for key, value in sorted(config.items()):
        print(f"  {key}: {value}")
    print()


# Initialize config on module import
try:
    if not CONFIG_FILE.exists():
        init_config()
except Exception as e:
    logger.debug(f"Could not auto-initialize config: {e}")
