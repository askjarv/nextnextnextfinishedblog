---
title: "Enabling root SSH login on an ESX host"
date: 2011-03-09
---

The oldies are the best ones - I always forget this when I get stumped by weird vRanger/vReplicator issues- from VMware.com:

Details

This article provides steps to use SSH to login to an ESX host as the root user.

Solution

Since ESX 3.0, for increased security, SSH is disabled by default for the root account on an ESX host. That is, the actual sshd service does not allow root logins. Non-root users are able to login with SSH. This is another layer of protection in addition to the host firewall.

**Note**: Each SSH connection to an ESX host uses additional Service Console resources. Use caution when using scripts or third party software that create multiple SSH sessions to the ESX Service Console. Excessive use of SSH on an ESX machine may cause the service console to exhibit symptoms of memory exhaustion.

To enable root login for SSH and SCP clients:

1. If you have physical access to the ESX host, login to the console of your ESX host as the root user. If you can only connect to the ESX host over the network, connect using an SSH client (such as PuTTY) and log in as a user other than root.
    
    To create a user in ESX host for using a SSH client:
    1. Log in to the vSphere Client as a root user.
    2. Click **Users & Groups**.
    3. Right-click on a blank area and click **Add**.
    4. Enter a username and password. Confirm your password.
        
        **Note**: Starting in ESX 4.0, the password needs to be at least 8 characters in length.
    5. Select **Grant shell access to this user** and click **OK**.
2. After you are logged in SSH session, switch to the root user with the command:
    
    su -
    
    **Note**: If you do not have any other users on the ESX host, you can create a new user by connecting directly to the ESX host with VMware Infrastructure (VI) or vSphere Client. Go to the **Users &** **Groups** tab, right-click on the Users list and select **Add** to open the **Add New User** dialog. Ensure that the **Grant shell access to this user**option is selected. These options are only available when connecting to the ESX host directly. They are not available if connecting to vCenter Server.
3. Edit the configuration file for SSH with the command:
    
    nano /etc/ssh/sshd\_config
4. Find the line that starts with PermitRootLogin and change the no to yes. You can find this line about 2 pages down from the top. Save the file by first pressing **Ctrl-O** and then **Enter**. Exit with **Ctrl-X**.
5. Restart the sshd service with the command:
    
    service sshd restart
    
    **Note**: Alternatively, use the command:
    
    /etc/init.d/sshd restart

 

Taken from:[http://kb.vmware.com/selfservice/microsites/search.do?language=en\_US&cmd=displayKC&externalId=8375637](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=8375637)
