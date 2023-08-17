#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:08:47 2023

@author: ashishm
"""

import subprocess
import json

def check_and_install():
    # Define the list of packages
    conda_packages = ["pandas", "numpy", "matplotlib", "rtl-sdr"]
    pip_packages = ["Pyastronomy"]

    # Capture the list of installed conda packages
    result = subprocess.run(["conda", "list", "--json"], stdout=subprocess.PIPE)
    installed_packages = [package['name'] for package in json.loads(result.stdout.decode('utf-8'))]
    
    # Check and install missing conda packages
    for package in conda_packages:
        if package not in installed_packages:
            print(f"Installing {package}...")
            result = subprocess.run(["conda", "install", "-y", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))
            print(result.stderr.decode('utf-8'))
        else:
            print(f"{package} is already installed.")

    # Install pip packages
    for package in pip_packages:
        print(f"Installing {package} with pip...")
        result = subprocess.run(["pip", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
        print(result.stderr.decode('utf-8'))

    print("Process completed.")

if __name__ == "__main__":
    check_and_install()
