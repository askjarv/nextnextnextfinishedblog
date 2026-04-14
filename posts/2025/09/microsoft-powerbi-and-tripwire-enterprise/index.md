---
title: "Microsoft PowerBi and Tripwire Enterprise"
date: 2025-09-27
categories: 
  - "api"
tags: 
  - "powerbi"
  - "tripwire"
coverImage: "2025-09-10-20_01_39-te-example.png"
---

A common request I get is setting up Microsoft PowerBi with Tripwire Enterprise. Whilst we don't have an official "out-of-the-box" solution for this, TE's REST API makes this a pretty simple option to get started with even if you just want to use PowerBi's native web reporting:

- Choose "Add Data" and select Web

- Add a relevant URL for the dataset of interest in the API - e.g. https://yourwebserver/api/v1/nodegroups to get node groups

- Provide some suitable (basic) auth login details...

- And you're done!

Remember you'll want to factor in things like ensuring you have a valid SSL cert on your TE console matched to the connection address, that your account should be able to read from the data points and that, if you're using large data areas (like versions) you'll want to handle paging.

For those who prefer to look at the "code behind" the scenes, you'll end up with something like this for nodegroups from this aprpacoh:

```
letSource = Json.Document(Web.Contents("https://teconsole.munchkin-justice.ts.net:8443/api/v1/nodegroups")),#"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),#"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"description", "id", "importedTime", "modifiedTime", "name", "type"}, {"description", "id", "importedTime", "modifiedTime", "name", "type"}),#"Changed Type" = Table.TransformColumnTypes(#"Expanded Column1",{{"description", type any}, {"id", type text}, {"importedTime", type datetime}, {"modifiedTime", type datetime}, {"name", type text}, {"type", type text}})in#"Changed Type"
```

And here's some example report/dashboard screenshots I've created in the past to demo/inspire:

<figure>

[![](images/2025-09-10-20_01_39-te-example.png)](https://nextnextnextfinished.wordpress.com/wp-content/uploads/2025/09/2025-09-10-20_01_39-te-example.png)

<figcaption>

PowerBi Compliance Dashboard from Tripwire

</figcaption>

</figure>

<figure>

[![](images/2025-09-10-20_01_21-te-example.png)](https://nextnextnextfinished.wordpress.com/wp-content/uploads/2025/09/2025-09-10-20_01_21-te-example.png)

<figcaption>

PowerBi Change Audit Dashboard from Tripwire

</figcaption>

</figure>
