# Function to check if a package is installed
function Test-PackageInstalled {
    param([string]$packageName)

    $package = Get-Package $packageName -ErrorAction SilentlyContinue
    return [bool]($package -ne $null)
}

# Install a package using pip
function Install-PackageWithPip {
    param([string]$packageName)

    Write-Host "Installing $packageName using pip..."
    pip install $packageName
}

# Install a package using conda
function Install-PackageWithConda {
    param([string]$packageName)

    Write-Host "Installing $packageName using conda..."
    conda install $packageName -y
}

# Add the conda-forge channel
Write-Host "Adding conda-forge channel..."
conda config --add channels conda-forge

# Check if pip is installed
if (!(Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "pip is not installed. Installing pip..."
    # Download the get-pip.py script and install pip
    Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
    python get-pip.py
    Remove-Item get-pip.py
    Write-Host "pip has been installed."
} else {
    Write-Host "pip is already installed."
}

# Dictionary to store package names and their corresponding installation commands
$packageCommands = @{
    "numpy" = @{ Conda = "conda install numpy -y"; Pip = "pip install numpy" };
    "matplotlib" = @{ Conda = "conda install matplotlib -y"; Pip = "pip install matplotlib" };
    "scipy" = @{ Conda = "conda install scipy -y"; Pip = "pip install scipy" };
    "rtl-sdr" = @{ Conda = "conda install -c conda-forge rtl-sdr"; Pip = "pip install rtl-sdr" };
    "PyAstronomy" = @{ Conda = ""; Pip = "pip install PyAstronomy" };
    "pandas" = @{ Conda = "conda install pandas -y"; Pip = "pip install pandas" };
}

# List of packages to check and install
$packages = @(
    "numpy",
    "matplotlib",
    "scipy",
    "rtl-sdr",
    "PyAstronomy",
    "pandas"
)

# Check and install packages
foreach ($package in $packages) {
    $condaCommand = $packageCommands[$package].Conda
    $pipCommand = $packageCommands[$package].Pip

    # Check if the package is already installed
    if (Test-PackageInstalled $package) {
        Write-Host "$package is already installed."
        continue
    }

    # Try installing with conda
    if ($condaCommand -ne "") {
        if (Install-PackageWithConda $package) {
            continue
        }
    }

    # If conda installation fails or conda is not available, try installing with pip
    if (Install-PackageWithPip $package) {
        continue
    }

    Write-Host "Failed to install $package using conda and pip."
}
