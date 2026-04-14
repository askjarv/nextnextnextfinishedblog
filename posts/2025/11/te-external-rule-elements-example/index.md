---
title: "TE External Rule Elements Example"
date: 2025-11-14
categories: 
  - "scripts"
tags: 
  - "tripwire"
---

  
One of the most powerful things I do with Tripwire Enterprise is add external sources to TE's change audit tracking. Whether it's an API, or a device with an unsupported SSH config, this workflow enables me to capture data and bring it along side all the rest of the compliance and change audit workflows that TE manages.

## Why this approach

Reasons for using this approach includes:

- Supporting external application information gathering for custom applications such as databases, web API’s, etc.

- Supporting protocols not available in Tripwire Enterprise’s native toolset (particular SSL ciphers, etc)

## Methodology

The method uses leverages a few components:

- The Tripwire Enterprise API via TE Commander, a command line utility available for Tripwire Enterprise. Note it's entirely possible to do this directly via the REST API (with your preferred tooling, be that bash scripting, python, powershell).

- (Optionally) A custom node is configured to reflect where the changes occur

- An External Rule is created to store configuration information

- An Command Output Capture Rule (COCR) is created to:
    - (If required) Connect to the custom device
    
    - Execute an element information gathering command and stores it to disk in a temporary file on the Tripwire Enterprise Server
    
    - The COCR subsequently captures the content of the temporary file and uploads it to the Tripwire Enterprise console via the API against the external rule (noted above)
    
    - The COCR finally removes the temporary file.
    
    - A check task is configured to regularly execute the COCR (noted above) against the Tripwire Enterprise console server.

## Known Limitations

The custom device configuration will be stored on disk (briefly) during the process (the file could be tampered with)

The preferred method for authentication is via a private key stored and used by the Tripwire Enterprise account to connect. If need be, a password could also be provided in the of a Tripwire Enterprise global variable passed via sshpass to provide authentication (this risks the root on the TE host having a password stored in its command history).

Any existing configuration history will be stored as a separate element from new elements created via this method (a new rule and element is required to store the configuration). This may require reconfiguring any policies built for the devices (if any)

## Configuration Planning

### Prerequisites

The following technical prerequisites are required:

- Tripwire Enterprise 8.6.0 or greater is required

- TE Commander 8.7.0 or greater is required

- TE Commander should be setup and configured as per the installation guide

- A suitable authentication account for TE Commander should be configured and accessible

- A suitable authentication account, preferably using SSH Private Key authentication, is required for the target device.

Note: The following guide is based on a deployment on Linux.

## About this Guide’s Example

The following sections walk through configuring an example device, a FortiNet FortiGate firewall, for monitoring. The example guidance is based around using Tripwire Enterprise 8.7.0 installed on Red Hat Enterprise Linux 7.2. TE Commander 8.7.0 is deployed to the Tripwire Enterprise console server. A Private Key for authentication has been configured to provide password authentication.

## Information Gathering

The following section contains a list of all the information that should be gathered ahead of the implementation of the custom rule to simplify the deployment. The example values given reflect the setup in the rest this guide.

- TE Commander Install Path - e.g. /usr/local/tripwire/tecmdr - the path to the TE Commander installation

- TE Commander Auth file path - e.g. /usr/local/tripwire/tecmdr/config/te\_auth.xml - The path to the configuration file in which TE Commander’s credentials are stored

- TE Commander User - e.g. tecadmin - The username used by TE Commander

- TE Commander Password - e.g. YOURPASSWORD - The password used by TE Commander

- TE Console Server Hostname, e.g. localhost - The hostname or IP address of the Tripwire Enterprise console server

- Rule Group Name - e.g. Your App Rule Group - This is the rule group where your configuration will be stored against your custom device

- Rule Name e.g. Config Rule - This is the rule where your configuration will be stored against your custom device

- Custom Node Group - e.g. MyNodeGroup - Used to determine what devices the custom element should be added to assess

- Custom Node Make/Model/Version - e.g. Fortinet / FortiGate / v1.0 - These attributes can be set manually against the Custom Node type to reflect the make, model and version

- Custom Node Username Global Variable Name - e.g. fortinet\_user - The name of the global variable used to store the Custom Node Username (see below)

- Custom Node Username e.g. root - Stored in the Global Variable for the device

- Custom Node Password Global Variable Name e.g. If required, a device password may be stored as a global variable, although it is highly recommended that your use Private Key Authentication

- Custom Node Password - If required, a device password may be stored as a global variable, although it is highly recommended that your use Private Key Authentication

- Custom Node Command Global Variable Name e.g. fortigate\_command The name of the global variable used to store the Custom Node Configuration Command e.g. show full-configuration - The command to execute on the custom node device

- Custom Element Name - e.g. FortigateConfig The name of the element to be created holding the output of the Custom Node Configuration Command

## Configuration

### TECommander Pre-Configuration

For the purposes of this document, TECommander is presumed to be installed in the following path:

/usr/local/tripwire/tecmdr

If you have specified an alternative path, please ensure this is reflected throughout the following configuration steps.

#### Configure Authentication for TE Commander

TECommander should have authentication configured to authenticate via a configuration file:

/usr/local/tripwire/tecmdr/bin/tecommander.sh encrypt -M ../config/te\_auth.xml -P YOURPASSWORD

where YOURPASSWORD should be replaced with your password. Please see the TE Commander documentation for further information about

authentication options using the encrypt command.

NB: the following characters are NOT permitted in the te\_auth password:

$%&\*!\\

### Configure an External Rule

  
In order to store element versions against the custom device, it is necessary to add a new External Rule using the following TE Commander command

```
/usr/local/tripwire/tecmdr/bin/tecommander.sh createextrule -M ../config/te_auth.xml -Q -r ConfigRule -x "Root Rule Group"
```

where:

- ConfigRule is the desired name for the External Rule. Ensure you make a note of the value you set as this will be used later in the creation of the Monitoring Rule

- Root Rule Group is the desired Rule Group in which you wish to create the External Rule.

## Creating a Target node

If the node does not already exist, it should be created prior to the initial run of the Custom Device Monitoring.

### Creating a Custom Node Type

Log in to Tripwire Enterprise with an administrator account

Navigate to the Settings Manager

Select Monitoring > Custom Node Types from the tree pane

Click on the New Custom Node Type button

Enter the name of the device type and a suitable description

Click Finish

### Creating a Node

Log in to Tripwire Enterprise with an Administrator account

Navigate to the Nodes manager

From the button bar, click on New Node

From the Node Type selection window, select the custom node type created in the previous section

Click OK

In the new device wizard, enter the IP address or hostname of the custom device and a suitable description:

Click Next

On the connection method screen (since the connection won’t be established via the console, you may leave the default values set)

You can optionally continue through the remaining pages for the new device wizard to set any other settings you wish (e.g. the version make and model

values), otherwise click Finish to complete creating the device.

## Creating Global Variables for configuration parameters

Global variables can be created in Tripwire Enterprise to save re-entering values in rules, etc. For our example, two global variables will be set up, representing the following values:

- The username for accessing the target device – in our example we will use $(fortigate\_user)

- The configuration command to be sent to the target device – in our example we will use $(fortigate\_cmd)

The following steps walk through creating the username global variable and should be repeated for each required global variable for the rule setup:

Login to the Tripwire Enterprise web console with an administrator account

Navigate to Settings Manager

Select System > Global Variables

Click on New Text on the button bar to create a new text variable

Enter the name and description for the Global Variable

Click Next.

Enter the value (in this case, the username) for the global variable.

Click Finish to complete the global variable creation.

Repeat this process for all other remaining global variables required.

### Creating the Configuration Gathering Rule

1. Log in to Tripwire Enterprise with an administrator account

3. Navigate to the Rules Manager

5. Navigate to an appropriate Rule Group in which you want to create the configuration gathering rule.

7. On the button bar, click on New Rule

9. Select File Server > Command Output Capture Rule

11. Click Next

13. Set the name and description required for the rule

15. Set the Default Severity to 0 (this is only used to track our changes so changes needn’t be captured for this rule).

17. Optionally, Enable the Tracking Identifier (recommended).

19. Specify an Element Name of your choosing.

21. Click Next

23. On the command line field add

```
$(ScriptFile.sh) '$(fortigate_user)' '$(fortigate_cmd)'
```

13\. In the script field, enter the following script:

COCR Command

> !/bin/sh
> 
> Get list of devices in Node group:
> 
> /usr/local/tripwire/tecmdr/bin/tecommander.sh avlistassettags -M /usr/local/tripwire/tecmdr/config  
> /te\_auth.xml -w Test | grep Node: | cut -f 2 -d ':' > NodeList.txt
> 
> Loop to get device configurations for each IP
> 
> while read n; do  
> echo $n
> 
> Get Config
> 
> ssh -o StrictHostKeyChecking=no $1@$n > config.tmp << EOF  
> $2  
> exit  
> EOF

Set Config in TE

/usr/local/tripwire/tecmdr/bin/tecommander.sh createextcontent -M /usr/local/tripwire/tecmdr/config  
/te\_auth.xml -e FortigateConfig -F config.tmp -n $n -Q -r "ConfigRule"

Remove Config File

rm config.tmp  
done < NodeList.txt

Remove Node List

rm NodeList.txt  
where

  
FortigateConfig reflects the name of the Element you wish to store the configuration with.  
ConfigRule reflects the name of the External Rule created in the section “Configure an External Rule”  
Test reflects the name of the NodeGroup you wish to run the rule against  

If required, you may also need to configure:  
Config.tmp to reflect your desired temporary file name for storing the configuration  
/usr/local/tripwire/tecmdr/ to reflect the path to the tecommander.sh for execution and te\_auth.xml file for authentication

Click Next

If required, add any Search and Replace Patterns and Actions, otherwise click Finish.

##   
Configuring a Check Task

In order to capture updated configuration information on a regular basis, a Check Task should be created to capture to execute the Rule created.  
Log in to Tripwire Enterprise with an administrator account  
  
Navigate to the Tasks Manager  
From button bar, chose New Task  
Chose a Check Rule Task type  
Click OK  
Configure a suitable Name, Description, Run As User and timeout for the task  
Click Next  
Select the Tripwire Enterprise Console Server from the Node selector  
Click Next  
Select the Config Capture rule created in the section entitled “Creating the Configuration Gathering Rule”  
Click Next  
Select the schedule you wish to run the check task  
Click Next  
You should not apply actions to this task, as changes will not be detected (since the element to be updated will be created against the External  
Rule).  
Click Next  
If desired, initialize the baselines, otherwise uncheck the option and allow the task to run as scheduled.  
Click Finish.

## Troubleshooting

The following troubleshooting steps are suggested to help identify common issues:

- Review the contents of the COCR rule – this will include any errors associated with connecting to the target device, uploading to the API via TECommander etc.

- Review the TECommander logs – typically these are located in the agent path of the TE Console.

- Try using static values, rather than global variables to ensure that expansion of the global variables is not resulting in errors.

- Ensure you are reviewing the correct element – data is stored against the device.
