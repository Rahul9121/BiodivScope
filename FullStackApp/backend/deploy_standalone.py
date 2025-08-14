#!/usr/bin/env python3
"""
Standalone deployment script for Railway
This creates a clean backend deployment without Node.js interference
"""

import os
import subprocess
import shutil
from pathlib import Path

def create_standalone_backend():
    """Create a standalone backend directory for Railway deployment"""
    
    # Create deployment directory
    deploy_dir = Path("../backend_deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Files to copy
    files_to_copy = [
        "app.py",
        "app_prod.py", 
        "config.py",
        "requirements.txt",
        "Procfile",
        "runtime.txt",
        "nixpacks.toml",
        ".env.example",
        ".railwayignore"
    ]
    
    # Directories to copy
    dirs_to_copy = [
        "routes",
        "database", 
        "api",
        "utils",
        "services",
        "ML Strategy"
    ]
    
    # Copy files
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, deploy_dir / file)
            print(f"✓ Copied {file}")
    
    # Copy directories
    for dir_name in dirs_to_copy:
        if Path(dir_name).exists():
            shutil.copytree(dir_name, deploy_dir / dir_name)
            print(f"✓ Copied directory {dir_name}")
    
    # Copy specific Python files
    python_files = [
        "mitigation_action.py",
        "report_generation.py"
    ]
    
    for py_file in python_files:
        if Path(py_file).exists():
            shutil.copy2(py_file, deploy_dir / py_file)
            print(f"✓ Copied {py_file}")
    
    print(f"\n🎉 Standalone backend created in: {deploy_dir.absolute()}")
    print("\nNext steps:")
    print("1. Create a new GitHub repository for the backend")
    print(f"2. Upload contents of {deploy_dir} to the new repository")
    print("3. Deploy the new repository to Railway")
    
if __name__ == "__main__":
    create_standalone_backend()
