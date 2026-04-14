---
title: "SSL VPN Auth by Security Group using LDAP on FortiGate OS 4.0MR2"
date: 2011-03-03
categories: 
  - "fortigate"
tags: 
  - "authentication"
  - "vpn"
---

**1) Create a standard active directory user object to allow the FortiGate to run LDAP queries**

In this example we are using the following:

User Name: Fortinet LDAP  
Username: fortinet  
Password: (something verify complex)  
Password never expires: Enabled  
User cannot change password: Enabled

**2) Create an Active Directory security group**

Users who are members of this group will be allowed to authenticate to the SSL VPN.  
For this example we are using: **SSL VPN Users**

**3) Add the LDAP server to the Fortigate appliance**

To speed things up we are using the CLI. You will require the following information to complete this step:

Pick an LDAP ID Name: **serverLDAP  
**LDAP Server (domain controller): **10.200.1.10  
**CNID

Allows you to choose what values are to be referenced when authenticating. In this example, we are using staff usernames (ie. jsmith):CNID = **sAMAccountName**

Distinguished Name

A distinguished name is path the OU or domain you wish to filter. In most cases using the entire domain is sufficient and will not affect performance (less than 1000 users). For this case we will be using a default instance, please replace domain.com with your own details.

DN: **DC=domain,DC=com**

LDAP Auth Type (basic, regular, anonymous)

**Use regular**, it requires a valid user ID to make LDAP queries.

AD Username

You will need the LDAP path to the "Fortinet LDAP" user object created in section 1. Load the command prompt on your domain controller:  
dsquery user -name "Fortinet LDAP"

which will return the value you need:

"CN=Fortinet LDAP,OU=Users,DC=domain,DC=com"

Now that you've acquired all the information, you can generate the required entry into the Fortinet CLI:

config user ldap

edit "serverLDAP"

set server "10.200.1.10"

set cnid "sAMAccountName"

set dn "dc=domain,dc=com"

set type regular

set username "CN=Fortinet LDAP,OU=Users,DC=domain,DC=com"

set password

next

end

**4) Create a firewall user group**

This group is used when creating your SSL VPN firewall policies.

You will require the following information to complete this task:

Group Name: **LDAP VPN Users**Pick a name to reference in future tasks. Tunnel Type: **Tunnel-Access**You can create unique tunneling policies by visiting (VPN->SSL->Portal). We will use the default tunnel-access for this task. If you would like to setup split tunneling, you will need to visit the "tunnel access" profile and enable it. LDAP Server Profile Name (created in section 3)**serverLDAP** Security Group LDAP pathThis is the important part! You need to acquire the exact LDAP path to the security group you are using to allow access to the SSL VPN. In this example, we created this security group in section 2.

To find it, use dsquery. Load the command prompt on your domain controller:  
dsquery group -name "SSL VPN Users"

which will return the value you need:

"CN=SSL VPN Users,OU=Builtin,DC=domain,DC=com"

Now that you've acquired all the information, you can enter the details into the Fortigate CLI: :

config user group

edit "SSL VPN Users"

set sslvpn-portal "tunnel-access"

set member "serverLDAP"

config match

edit 1

set server-name "serverLDAP"

set group-name "CN=SSL VPN Users,OU=Builtin,DC=domain,DC=com"

next

end

next

end

**5) Create an incoming firewall policy to open the SSL VPN Auth mechanism**

Generally most situations call for WAN1 to Internal1. Depending on your network, you may need to setup several incoming rules if you would like to allow authenticated users to access internal WLAN or other internal interfaces. For this example, we will just create the standard.

Using the Web-Gui:

\- Firewall -> Policy -> Policy -> Create New

Source Interface: WAN1  
Source Address: All  
Destination Interface: Internal1  
Destination Address: ALL or Internal LAN  
Action: SSL-VPN

At this point you will notice the form change.

\- Click for the "Add" button located directly below "Configure SSL-VPN Users".

\- Move "LDAP VPN Users" to the available user groups

\- Move "Any" to the selected services.

\- Save.

\- Save the new firewall policy.

\- Move it to the top of the "Wan -> Internal" list so that this new policy is the first.

**6) Create a firewall policy to allow the authenticated users to access your internal network.**

Once users are authenticated, they need access to the internal lan. Create another policy as follows:

Source Interface: SSL Tunnel Interface  
Source Address: All  
Destination Interface: Internal1  
Destination Address: ALL or Internal LAN  
Action: Accept

This allows all SSL traffic to pass to all internal LAN IPs

**7) Add users to the security group and test**

Remember that each user with access to the VPN needs to be a member of the security group in section 2. Once added, you can load the SSL VPN client from an external location and attempt a connection.

Server: (your external ip or hostname)  
Username: (active directory username)  
Password: (active directory password)
