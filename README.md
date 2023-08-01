# Hline-analysis-tool
rtl-sdr based 21 cm hydrogen line recording and analysis GUI tool.
Required Anaconda/Miniconda installed.

Download the files to your local computer.

Install Anaconda / miniconda

After installation open anaconda/miniconda terminal and follow the steps below depending on OS.

A) Windows installation:
	
	# run following commands (without serial numbers) in anaconda/miniconda terminal

	1. cd C:\Users\YourUsername\Scripts
	# choose the anaconda or miniconda check_and_install_packages.ps1 depending on anaconda or miniconda in the.
	# replace YourUsername\Scripts with path to the appropriate script.
	
	2. powershell.exe -ExecutionPolicy Bypass -File check_and_install_packages.ps1
	# replace check_and_install_packages.ps1 with appropriate file name. These are one time install requirements.

 	3. Use zadig to replace rtl2832u driver.
  
	run gui with the following command in anaconda/miniconda terminal.
	4. python GUI.py
	# you need not run step 1 and 2 again. Only run step 3 in anaconda/miniconda terminal to run GUI.	

B) Linux/Mac
	
	# run following commands (without serial numbers) in anaconda/miniconda terminal.

	1. cd to check_and_install_packages.sh file.
	2. sudo chmod +x check_and_install_packages.sh
 	3. (For linux) if required, blacklist rtl2832 driver. Details can be found at (https://sdr-enthusiasts.gitbook.io/ads-b/setting-up-rtl-sdrs/blacklist-kernel-modules).
	4. python ./GUI.py

	# you need not run step 1 and 2 again. Only run step 3 in anaconda/miniconda terminal to run GUI.	
	
