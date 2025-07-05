#!/usr/bin/env python3
"""
Convenience wrapper for the main start script.
This maintains backward compatibility while redirecting to the new structure.
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Run the actual start script from the scripts/maintenance directory."""
    script_path = Path(__file__).parent / "scripts" / "maintenance" / "start.py"
    
    if not script_path.exists():
        print(f"❌ Error: Start script not found at {script_path}")
        print("Make sure the project structure is correct.")
        sys.exit(1)
    
    print("🔄 Redirecting to scripts/maintenance/start.py...")
    
    # Pass all arguments to the actual script
    cmd = [sys.executable, str(script_path)] + sys.argv[1:]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
