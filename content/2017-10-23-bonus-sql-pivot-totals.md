---
title: "Bonus SQL Pivot (% totals)"
date: 2017-10-23
categories: 
  - "sql"
---

Probably something you'll want to do is summarise the pivot tables I noted earlier. That's not too hard - but you'll need to add an additional column to do you summing on (I reused IP since my table had no ID's to count):

```
SELECT r2.IP,     
[Passed] AS Pass,     
[Failed] as Fail, 
ROUND(([Passed] / CAST(([Passed] + [Failed]) AS REAL)) * 100, 0) AS PercentPassed, 
   ROUND(([Failed] / CAST(([Passed] + [Failed]) AS REAL)) * 100, 0) AS PercentFailed 
FROM    (SELECT IP As ID, IP, [TestResult] FROM #temptable1) r1
PIVOT (Count(ID) FOR [TestResult] IN ([Passed], [Failed])) AS r2
```

Just want the percent? Just drop the pass and fail columns:

```
SELECT r2.IP,
ROUND(([Passed] / CAST(([Passed] + [Failed]) AS REAL)) * 100, 0) AS PercentPassed,    
ROUND(([Failed] / CAST(([Passed] + [Failed]) AS REAL)) * 100, 0) AS PercentFailed 
FROM    (SELECT IP As ID, IP, [TestResult] FROM #temptable1) r1
PIVOT (Count(ID) FOR [TestResult] IN ([Passed], [Failed])) AS r2
```

Finally, maybe you want to include Inconclusive results as failures for the purposes of summarising- in which case you'll end up with:

```
SELECT a2.IP,     
[Passed] AS Pass,     
[Failed] as Fail, [Inconclusive] as Inconclusive,    
ROUND(([Passed] / CAST(([Passed] + ([Failed]+[Inconclusive])) AS REAL)) * 100, 0) AS PercentPassed,    
ROUND((([Failed] + [Inconclusive]) / CAST(([Passed] + ([Failed]+[Inconclusive])) AS REAL)) * 100, 0) AS PercentFailed 
FROM    (SELECT IP As ID, IP, [TestResult] FROM #temptable1) a1 -- We need to have a unique ID value to count, but we'll just use IP again!
PIVOT (Count(ID) FOR [TestResult] IN ([Passed], [Failed], [Inconclusive])) AS a2
```
