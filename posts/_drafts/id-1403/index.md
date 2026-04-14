---
title: "Setting up OpenSSH on Windows Server (2019+) for Tripwire IP360 Backup Targets"
tags: 
  - "ip360"
  - "tripwire"
  - "tripwire-ip360"
draft: true
---

This is potentially helpful if you're looking to backup or migrate from IP360 and need a backup (and generally handy to know as it's not much publicized IMHO!)... Since Microsoft Server 2019+ now officially supports OpenSSH we now have a viable option for Windows people who want to backup their IP360 VnE's without spinning up a dedicated Linux box. But managing the keys is somewhat different / unfamiliar with Windows admins, so here is the process you'll need to follow to set up your IP360 and Windows server for backups:

## Install

To install OpenSSH using PowerShell, first launch PowerShell as an Administrator. To make sure that the OpenSSH features are available for install:

```
Get-WindowsCapability -Online | ? Name -like 'OpenSSH*'# This should return the following output:#Name : OpenSSH.Client~~~~0.0.1.0 State : NotPresent#Name : OpenSSH.Server~~~~0.0.1.0 State : NotPresent
```

Then, install the server and/or client features:

```
# Install the OpenSSH ClientAdd-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0# Install the OpenSSH ServerAdd-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0# Both of these should return the following output:#Path :#Online : True#RestartNeeded : False
```

Initial Configuration of SSH Server

To configure the OpenSSH server for initial use on Windows, launch PowerShell as an administrator, then run the following commands to start the SSHD service:

```
Start-Service sshd# OPTIONAL but recommended:Set-Service -Name sshd -StartupType 'Automatic'# Confirm the Firewall rule is configured. It should be created automatically by setup.Get-NetFirewallRule -Name *ssh*# There should be a firewall rule named "OpenSSH-Server-In-TCP", which should be enabled# If the firewall does not exist, create oneNew-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -ProtocolTCP -Action Allow -LocalPort 22
```

## Get your IP360 Key

1. Log in to IP360 web interface

3. Go to Settings> System Settings > Automated Scan Exports ![Image](images/c79bd45b-364e-4767-a053-8c7ccb2ab8d4) 

5. Click on Modify and set the desired settings - bear in mind you will want to use some specific options to reflect your Windows host - namely:
    1. The host IP should be your Windows backup server IP
    
    3. The protocol should be SSH1 RSA (SCP) - SSH2 DSA, etc are deprecated and have to be manually enabled in Open SSH
    
    5. The Directory should reflect your Windows path where you want backups to go - but with FORWARD SLASHES - e.g. C:\\Backup becomes C: /Backup: ![Image](images/bf05bb0c-b019-47b9-8ded-55352c695778) 

7. Once you have this, click on the "inline" link to grab your key file

9. Open the file (in notepad) and copy the value - you'll use this on your Window host

## Setting up your Windows Host

Non-Admin Users: If your user account is not a local/domain admin (generally recommended!) you can add a user and SSL key by doing the following:

1. Create the directory you want your backup to be stored in - in my case, I've opted for C:\\Backup

3. Add the user
    1. Add a Windows user in the normal way- I've created one called IP360User:  
        net user ip360user /add
    
    3. Log in to the server as the user (to create the user's profile)

5. Add the SSL key
    1. Open Explorer and navigate to your profile folder on the server, such as C:\\Users\\ip360user\\.ssh
    
    3. Look for a .ssh folder. If one doesn't exist, create it.  
        Note: Windows Explorer won't let you create the folder with the name ".ssh". Instead, use ".ssh." with an extra dot at the end. The extra dot will be removed, and you'll have a folder correctly named .ssh
    
    5. In the .ssh folder, create a new text document named "authorized\_keys" and open it with Notepad. If the file already exists, just open it.  
        Note, this file has no extension. You may need to make file extensions visible to ensure you remove the .txt extension
    
    7. In Notepad, paste the key you copied earlier and save the file. If there was already a key in this file, paste your key onto a new line below the existing one.

## Testing

With this in place you can use the test function :

![Image](images/58908a13-737c-4309-aaaf-60b7911fb85d)

and it will generate a file:

![Image](images/1f94e277-71c7-42a3-a916-95ab14a5110f)

## Admin Users

If the user account on the server you are connecting to is in the local Administrators group, the public key must be placed in the C: \\ProgramData\\ssh\\administrators\_authorized\_keys instead of the user's .ssh folder. Additionally, only the Administrators group and SYSTEM account can have access to that file, for security purposes. After copying your key into the file and saving it, you can use this script to set the correct permissions on it. Here are the complete steps

1. Open the public key file in Notepad. If using default path, it is C:\\Users\\myuser\\.ssh\\id\_rsa.pub

3. Copy the contents of the file to clipboard. Ensure you get the entire file.

5. Connect to the server

7. Open Notepad as administrator

9. In Notepad, paste in the key you copied earlier

11. Save the file as C:\\ProgramData\\ssh\\administrators\_authorized\_keys with no extension. You may need to make file extensions visible to ensure you can remove the .txt extension.

13. Use the below PowerShell script to set the correct permissions on the file

```
$acl = Get-Acl C:\ProgramData\ssh\administrators_authorized_keys$acl.SetAccessRuleProtection($true, $false)$administratorsRule = New-Object system.security.accesscontrol.filesystemaccessrule("Administrators","FullControl","Allow")$systemRule = New-Object system.security.accesscontrol.filesystemaccessrule("SYSTEM","FullControl","Allow")$acl.SetAccessRule($administratorsRule)$acl.SetAccessRule($systemRule)$acl | Set-Acl
```

If you don't do this, and instead only place the file in the .ssh folder for the user, you'll either get prompted for your password (instead of using the key file), or your connection will fail with "Too many authentication attempts".

## Setting up your backup to push

1. Log in to IP360 again

3. Navigate to Settings > Database > Status and click modify to set the remote backup/archive settings ![Image](images/7cdb1f36-04ff-4cca-986c-a85911986936) 

5. Click Submit

7. Go to the backup and Click enable.

9. Fill in the details for your connection (these should match the settings above! ![Image](images/04ff3ead-d321-4227-8f60-432cd7c41176) 

## Troubleshooting

By default, logs are added to Event Viewer:![Image](images/9ded8c79-9f9c-45cb-981e-bbe27f54c3b6) You can enable debug logging to file )and enable debug logging) by:

1. Open up sshd\_config (by default, in C:\\ProgramData\\ssh).

3. Edit the logging section to set  
    SyslogFacility   
    and   
    LogLevel

![Image](images/c0a2102f-172d-4d6c-8dd4-ab49e86dbb6a)
