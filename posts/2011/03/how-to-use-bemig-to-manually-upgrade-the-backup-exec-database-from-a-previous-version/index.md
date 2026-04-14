---
title: "How to use BEMIG to manually upgrade the Backup Exec database from a previous version"
date: 2011-03-03
categories: 
  - "backup-exec"
tags: 
  - "utils"
---

##### Problem

Need to manually upgrade Backup Exec from a previous version.

##### Solution

The recommended upgrade method is to allow the Backup Exec (BE) installer upgrade BE and its database during the installation. If that fails to occur or a saved database from a previous BE version needs to be added to a newer BE version, the BEMIG tool can be used. This tool follows the same upgrade version rules that the BE installer has. This is noted in the chart below.

Note: If the .mdf and .ldf files are from an older version of Backup Exec installed on a different server then please do not follow the procedure below if any of the following are true:

- Backup Exec is clustered.
- The Backup Exec Shared Storage Option (SSO) is installed.
- The Backup Exec Server Free Option is installed.
- The computer where Backup Exec is installed and the computer where it will be installed are running two different versions of the Windows Operating System.
- If planning to move Backup Exec to a different drive/directory on the server.
- If upgrading from one version/revision (build) of Backup Exec to another

Steps:  
1\. Confirm BE is working in its current database first.  
2\. Stop the all Backup Exec services (including the  SQL(BKUPEXEC) service)

3\. Open the \\Program Files\\Symantec\\Backup Exec Directory.  Copy the Data folder and paste it in the same location. Rename the "Copy of Data" to "Data-'TodaysDate' or "Data-Version#-New"  
4\. Copy the saved Database from the previous BE version into the Backup Exec\\Data folder.  
   This will be **bedb\_dat.mdf** and **bedb\_log.ldf** files.  
5\. If the Catalogs have been saved also, rename the Catalogs to Catalogs.old, then copy/move the saved catalogs under Backup Exec.  
6\. Start the SQL service.  
7\. Set the registry keys for BEMIG.  
**_Warning_:** _Incorrect use of the Windows registry editor may prevent the operating system from functioning properly. Great care should be taken when making changes to a Windows registry. Registry modifications should only be carried-out by persons experienced in the use of the registry editor application. It is recommended that a complete backup of the registry and workstation be made prior to making any registry changes._

7a. Launch the Registry Editor (Start, Run, Regedt32).    
     Navigate to **HKLM | Software | Symantec | Backup Exec for Windows | Backup Exec | _"VersionNumber"_ | Install**  
![](images/287063.jpg)  
7b. Modify the value of "Upgrade" to 1. 
      (Create as a Dword if it is not present)  
7c. Modify the value of  "Upgrade Version" to the version of the DB being imported. See chart.  
      (Create as a String value if not present)   
**Please refer the following Table while setting the value for Upgrade version Key.  
**

**PRODUCT VERSION**  
**UPGRADE VERSION**  
**10**  
**10D**  
**11**  
**11D**  
**12.0**  
**12.5**  
**2010**  
**2010 R2**

9.1 revison 4691  
9.1.4691.0  
X  
X  
X

10.0 revison 5484  
10.0.5484.0  
X  
X  
X

10.0 revison 5520  
10.0.5520.0  
X  
X

10.1 (10d) revison 5629  
10.1.5629.0  
X  
X  
X

11 revison 6235  
11.0.6235.0  
X  
X

11 (11d) revison 7170  
11.0.7170.0  
X  
X  
X  
X

12.0 revison 1364  
12.0.1364.0  
X  
X  
X

12.5 revison 2213  
12.5.2213.0  
X  
X

2010 revison 2896  
13.0.2896.0  
X

2010 R2 revison 4164  
13.0.4164.0

8.Open a CMD command prompt to \\Program Files\\Symantec\\Backup Exec  
  Run BEMIG  
  Wait for it to fully complete and return to a new prompt.  
9\. Start BE services and open the BE console.  
Note, if the services fail to start, you may need to do additional steps of:

1. Stop the SQL(BKUPEXEC) service
2. Copy the BEDB database files from the Data folder to the desktop
3. Start the SQL(BKUPEXEC) service
4. Run BEutility Copy Database to import the desktop BEDB files. This will correct any Environmental changes effecting the database.    
               Copy Database Document -  [http://support.veritas.com/docs/286093](http://support.veritas.com/docs/286093)

##### Article URL [http://www.symantec.com/docs/TECH50537](http://www.symantec.com/docs/TECH50537)
