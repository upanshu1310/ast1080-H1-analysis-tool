# Hline-analysis-tool
rtl-sdr based 21 cm hydrogen line recording and analysis GUI tool.
Required Anaconda/Miniconda installed.

Download the files to your local computer.

Install Anaconda / miniconda

After installation open anaconda/miniconda terminal and follow the steps below depending on OS.

A) Windows installation:
	
	# run following commands (without serial numbers) in anaconda/miniconda terminal.

	1. cd C:\Users\YourUsername\Scripts
	# replace YourUsername\Scripts with path to the appropriate script. eg cd C:\Users\YourUsername\Desktop\Hline-analysis-tool.
	
	2. powershell.exe -ExecutionPolicy Bypass -File windows_miniconda_install_packages.ps1
	# replace windows_miniconda_install_packages.ps1 with windows_anaconda_install_packages.ps1 if you are using anaconda. These are one time install requirements.

 	3. Use zadig to replace rtl2832u driver.
  		a. Connect the RTL-SDR dongle to the USB port.
        	b. Download zadig driver installer from \url{https://zadig.akeo.ie}.
        	c. Run zadig as administrator.
        	d. Select rtl2832u driver from dropdown list.
        	e. If you dont see rtl2832u listed then go to options, tick List All Devices and untick Ignore Hubs or Composite Parents.
        	f. After selecting the driver, click on Install Driver. Installation should take few minutes. Do not unplug RTL-SDR untill installation is complete.
  
	run gui with the following command in anaconda/miniconda terminal.
	4. python GUI.py
	# you need not run step 1, 2 and 3 again. Only run step 4 in anaconda/miniconda terminal to run GUI.	

B) Linux/Mac
	
	# run following commands (without serial numbers) in anaconda/miniconda terminal.

	1. cd to linux_mac_install_packages.sh file.
	2. sudo chmod +x linux_mac_install_packages.sh
 	3. (For linux) if required, blacklist rtl2832 driver. Details can be found at (https://sdr-enthusiasts.gitbook.io/ads-b/setting-up-rtl-sdrs/blacklist-kernel-modules).
	4. python ./GUI.py

	# you need not run step 1, 2 and 3 again. Only run step 4 in anaconda/miniconda terminal to run GUI.	
	
