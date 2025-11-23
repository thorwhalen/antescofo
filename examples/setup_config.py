#!/usr/bin/env env python
"""
Setup script for Antescofo configuration.

Run this script to initialize your ~/.config/antescofo directory
and create the default config file.

Usage:
    python examples/setup_config.py
"""

from antescofo.util import init_config, print_config, CONFIG_DIR, CONFIG_FILE
from pathlib import Path


def main():
    print("\n" + "=" * 70)
    print("        ANTESCOFO CONFIGURATION SETUP")
    print("=" * 70)

    print(f"\nThis script will create your Antescofo configuration at:")
    print(f"  {CONFIG_FILE}")

    # Check if config already exists
    if CONFIG_FILE.exists():
        print(f"\n⚠️  Config file already exists!")
        response = input("Overwrite existing config? (y/N): ").strip().lower()
        if response != 'y':
            print("\nCancelled. Using existing config.")
            print_config()
            return
        force = True
    else:
        force = False

    # Initialize config
    print(f"\n[SETUP] Creating config directory: {CONFIG_DIR}")
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[SETUP] Writing default config to: {CONFIG_FILE}")
    init_config(force=force)

    print("\n✓ Configuration created successfully!")

    # Display config
    print_config()

    # Provide next steps
    print("\nNEXT STEPS:")
    print("=" * 70)
    print("1. Edit the config file if needed:")
    print(f"     {CONFIG_FILE}")
    print("\n2. Key settings to verify:")
    print("   - antescofo_send_port: Port where Antescofo listens (default: 5678)")
    print("   - python_receive_port: Port where Python receives events (default: 9999)")
    print("   - pd_listen_port: Port where PD synth listens for OSC (default: 10000)")
    print("   - pd_patch_path: Path to your pd_synth_patch.pd file")
    print("\n3. Run the demo:")
    print("     python examples/run_demo.py")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
