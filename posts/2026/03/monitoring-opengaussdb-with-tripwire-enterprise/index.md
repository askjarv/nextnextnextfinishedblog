---
title: "Monitoring OpenGaussDB with Tripwire Enterprise"
date: 2026-03-25
categories: 
  - "fim"
  - "scm"
tags: 
  - "database"
  - "gaussdb"
  - "tripwire"
coverImage: "pexels-photo-6549358.jpeg"
---

I've not done much with GaussDB/OpenGaussDB, so figured I'd post the process I used to setup some monitoring including the deployment itself.

### Installing OpenGaussDB

Currently, it seems as if OpenGaussDB's preferred Linux version is a Centos 7.6 build, so I started with a quick deployment. From there we can:

- Download the installation media ([https://opengauss.org/en/download/](https://opengauss.org/en/download/)) and unzip to somewhere appropriate.

- Quick off the installer from the simpleInstall path with _sh install.sh -w "MyPasswordHere"_

- NB: From the wizard, I deployed their test DB's when prompted (if you want to follow on exactly)!

- Given I'd not done any other setup on the host, to get going I also need to install OpenSSL by downloading teh zip (in this case, for compatibility, I went old - I'd recommend to others using what's appropriate for you) and unpacking and deploying it: _./config --prefix=/usr --openssldir=/etc/ssl --libdir=lib no-shared zlib-dynamic_

- From there, I could hop into the guassdb bin directory and run ./gs\_ctl query -D /mypath/single\_node.

### Checking our Command Output Capture Rules will work from our agent

With that all set, I can configure some basic Command Output Capture Rules to capture relevant audit output info - let's start with checking our DB structure:

```
./gsql school -P pager=OFF -c "SELECT table_schema, table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'"
```

should give us a simple list of tables in the school DB - note the _\-P pager=OFF_ - we don't our data paged in Tripwire since this is going to be collected non-interactively! Our sample DB doesn't include a lot of exciting data - but we can, of course, do an audit of, say, a particular table:

```
./gsql school -P pager=OFF -c "SELECT * from course"
```

or, from the other sample DB we could collect card data- of course, we probably wouldn't do this for change audit:

```
./gsql finance -P pager=OFF -c "SELECT * from bank_card"
```

Since our typical goal is auditing, instead, we can use some of the following queries:

## Authentication & Access Control

### List all roles and attributes

```
SELECT rolname,       rolsuper,       rolcreaterole,       rolcreatedb,       rolcanlogin,       rolreplication,       rolbypassrlsFROM pg_rolesORDER BY rolname;
```

### Roles with superuser privileges (high risk)

```
SELECT rolnameFROM pg_rolesWHERE rolsuper = true;
```

### Roles that can login

```
SELECT rolnameFROM pg_rolesWHERE rolcanlogin = true;
```

### Check password validity / expiry (if configured)

```
SELECT rolname, rolvaliduntilFROM pg_authidWHERE rolcanlogin = true;
```

* * *

# Privileges & Permissions

### Database-level privileges

```
SELECT datname,       pg_catalog.pg_get_userbyid(datdba) AS owner,       dataclFROM pg_database;
```

### Schema privileges

```
SELECT nspname,       nspowner,       nspaclFROM pg_namespace;
```

### Table privileges (who can access what)

```
SELECT grantee,       table_schema,       table_name,       privilege_typeFROM information_schema.role_table_grantsORDER BY grantee, table_name;
```

### Detect overly permissive tables (PUBLIC access)

```
SELECT table_schema, table_nameFROM information_schema.role_table_grantsWHERE grantee = 'PUBLIC';
```

# Configuration & Hardening

### Key security-related settings

```
SELECT name, settingFROM pg_settingsWHERE name IN (  'password_encryption',  'ssl',  'log_connections',  'log_disconnections',  'log_statement',  'log_min_duration_statement',  'pgaudit.log');
```

### Check SSL enforcement

```
SHOW ssl;
```

### Check password encryption method

```
SHOW password_encryption;
```

### Check listening addresses (exposure surface)

```
SHOW listen_addresses;
```

# Logging & Auditing

### Check logging configuration

```
SELECT name, settingFROM pg_settingsWHERE name LIKE 'log_%'ORDER BY name;
```

### Check if pgAudit extension is installed

```
SELECT * FROM pg_extension WHERE extname = 'pgaudit';
```

### Active sessions (who is connected now)

```
SELECT usename,       datname,       client_addr,       application_name,       stateFROM pg_stat_activity;
```

# Network Exposure & Connections

### Current connections by user

```
SELECT usename, count(*)FROM pg_stat_activityGROUP BY usename;
```

### Remote connections only

```
SELECT usename, client_addrFROM pg_stat_activityWHERE client_addr IS NOT NULL;
```

# Data Integrity & Ownership

### Tables without primary keys (risk for integrity/audit)

```
SELECT relnameFROM pg_classWHERE relkind = 'r'AND NOT EXISTS (  SELECT 1  FROM pg_index  WHERE pg_index.indrelid = pg_class.oid  AND pg_index.indisprimary);
```

### Table ownership

```
SELECT schemaname,       tablename,       tableownerFROM pg_tables;
```

# Default Privileges (often overlooked)

```
SELECT defaclrole::regrole,       defaclnamespace::regnamespace,       defaclobjtype,       defaclaclFROM pg_default_acl;
```

## Making it a template

Rather than using all these as one-liner COCR's which are hard to read, we can install pass in the SQL command as a parameter with a "Scripted" COCR - effectively :

```
gsql dbname -P pager=OFF < $(ScriptFile).sql
```

This makes it easy to duplicate and use as a template for setting up all your custom queries- you can even set a node level parameter for your DB so you can set it per host for ease!

I hope that helps you plan some of our future monitoring!
