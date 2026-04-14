---
title: "Checking mySQL privileges"
date: 2012-04-10
---

Again, just to show my lack of mySQL knowledge, I'm posting on what "should" be simple - checking why you can't access mySQL from a remote host.

First off, establish a session from the localhost using the mySQL command line (it's typically in the install directory)- the syntax is normally along the lines of:

```
mysql -u root -p
```

then check your user list and access IP's with the command

```
select User,Host from mysql.user;
```

Then, if, like me, you find you lack permissions, you can grant them, with the command:

```
GRANT ALL PRIVILEGES ON *.* TO USERNAME@IP IDENTIFIED BY "PASSWORD";
```

where Username is your desired username, ip is your connecting host IP, and Password is the desired password for your user. You may then want to run

```
FLUSH PRIVILEGES;
```

to apply the settings- then give it a go!
