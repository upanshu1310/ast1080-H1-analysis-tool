{\rtf1\ansi\ansicpg1252\cocoartf2707
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Check if pip is installed\
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) \{\
    Write-Host "Pip is not installed. Installing pip..."\
    Invoke-Expression "conda install pip -y"\
    Write-Host "Pip installed successfully."\
\} else \{\
    Write-Host "Pip is already installed."\
\}\
\
# List of required packages\
$packages = @(\
    "numpy",\
    "matplotlib",\
    "scipy",\
    "pandas",\
    "scikit-learn",\
    "rtl-sdr",\
    "PyAstronomy"\
)\
\
# Install missing packages\
foreach ($package in $packages) \{\
    if (-not (Get-Command $package -ErrorAction SilentlyContinue)) \{\
        Write-Host "Package $package is not installed. Installing..."\
        Invoke-Expression "pip install $package"\
        Write-Host "Package $package installed successfully."\
    \} else \{\
        Write-Host "Package $package is already installed."\
    \}\
\}\
}