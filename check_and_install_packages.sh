#!/bin/bash

# run following 2 commands in anaconda terminal before running the script.
# chmod +x check_and_install_packages.sh
# ./check_and_install_packages.sh

# Function to check if pip is installed
is_pip_installed() {
    command -v pip >/dev/null 2>&1
}

# Function to install pip
install_pip() {
    echo "Installing pip..."
    if python -m ensurepip; then
        echo "pip installed successfully."
    else
        echo "Error: Failed to install pip. Please install it manually."
        exit 1
    fi
}

# Check if pip is installed
if is_pip_installed; then
    echo "pip is already installed."
else
    install_pip
fi

# List of required packages
required_packages=("tk" "matplotlib" "pandas" "numpy" "PyAstronomy" "rtl-sdr")

# Function to check if a package is installed via conda
is_conda_package_installed() {
    conda list | grep -q "^$1 "
}

# Function to check if a package is installed via pip
is_pip_package_installed() {
    pip list | grep -q "^$1 "
}

# Function to install a package via pip
install_with_pip() {
    pip install "$1"
}

# Function to install a package via conda
install_with_conda() {
    conda install -y "$1"
}

# Check and install required packages
for package in "${required_packages[@]}"; do
    if is_conda_package_installed "$package"; then
        echo "$package is already installed via conda."
    elif is_pip_package_installed "$package"; then
        echo "$package is already installed via pip."
    else
        echo "Installing $package..."
        if install_with_conda "$package"; then
            echo "$package installed successfully via conda."
        elif install_with_pip "$package"; then
            echo "$package installed successfully via pip."
        else
            echo "Error: Failed to install $package. Please install it manually."
        fi
    fi
done

echo "All required packages are installed."
