---
title: "Exchange GRT restore Fails (Backup Exec)"
date: 2011-03-03
categories: 
  - "backup-exec"
tags: 
  - "exchange-2003"
  - "exchange-2007"
  - "exchange-2010"
  - "grt"
  - "restore"
---

After spending what seemed like an eternity with an extremely charismatic Symantec engineer looking at this issue, we found that the problem was that Trend was scanning the C:\\temp folder (default location for the GRT staging) during the backups.

This then caused issues in BE and was causing the jobs to fail.

The hotfix mentioned below was supposed to resolve this, but clearly does not always work.

All we did was add an exclusion to the Trend Real-Time scan to ignore this folder (C:\\temp) on the backup server and the backups started working with GRT turned on again.

Fortunately it’s also very easy (and better form) to modify where the GRT staging takes place (since the temp path is often exploited by viruses, etc)

You just need to create a new location for this to use (I just used C:\\Program Files\\Symantec\\GRT temp)

Then point Backup Exec to use this as the default location: Tools | Options, under the backup section at the bottom.

Once this is done, in Trend you just need to create the exception for the real-time scan in the Trend console, I used the drop down in the top left to modify the real-time scan settings for the backup servers only then added the exclusion as normal.
