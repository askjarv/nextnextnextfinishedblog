---
title: "SQL Pivots for the rest of us"
date: 2017-10-23
categories: 
  - "sql"
---

Every time I have to build a SQL pivot I can't remember how to do it and end up searching online and struggle to work out what the heck people are talking about in their examples and spend ages looking at "sales" data examples, etc. that are overly complicated for my simple pivot purposes so I'm posting this as an aide-memoire...

## Do I need to PIVOT - or can I summarise in some other way

First of all, double check if you really need a pivot table! SQL has nice summary functions available to you in the form of **group by** \- let’s assume you have some data that looks like (in a table we'll call #temptable1):

| **IP** | **TestResult** |
| --- | --- |
| **10.1.1.1** | Pass |
| **10.1.1.1** | Pass |
| **10.1.1.1** | Fail |
| **10.1.1.1** | Inconclusive |
| **10.1.1.2** | Pass |
| **10.1.1.2** | Fail |
| **10.1.1.2** | Pass |

Etc.

If I want a simple summary table I can do:

```
 select COUNT(IP) as Devices, [TestResult]
 from #temptable1
 Group by [TestResult]
```

to give me:

| **Devices** | **TestResult** |
| --- | --- |
| **4** | Pass |
| **2** | Fail |
| **1** | Inconclusive |

This gives us a good high level summary by aggregating (counting/summing the device count) - but not a lot of use if I want to get details for a specific IP address.

We could do:

```
 select ip, [Test State], COUNT(IP) as Total
 from #temptable1
 Group by ip, [Test State]
```

To give us

| **IP** | **TestResult** | **Total** |
| --- | --- | --- |
| 101.1.1 | Fail | 1 |
| 10.1.1.1 | Inconclusive | 1 |
| 10.1.1.1 | Pass | 2 |
| 10.1.1.2 | Fail | 1 |
| 10.1.1.2 | Pass | 2 |
|  |  |  |

...and we can even filter by IP:

```
 select ip, [Test State], COUNT(IP) as Total
 from #temptable1
 where ip = '10.1.1.1'
 Group by ip, [Test State]
```

To show a single host:

| **IP** | **TestResult** | **Total** |
| --- | --- | --- |
| 10.1.1.1 | Failed | 1 |
| 10.1.1.1 | Inconclusive | 1 |
| 10.1.1.1 | Passed | 2 |

But there are some limits here- for example, we might want to include an inconclusive score of "0" - in this summary if an IP has no inconclusive it simply won't show.

## ...A nasty way to brute force a solution...

OK, so we want to see the type of data we want- we could do a series of selects to give us the results we want:

```
select Count(#temptable1.[TestResult]) As Pass, Ip from #temptable1 
where [TestResult] = 'Pass'
and ip = '10.1.1.1'
group by IP

select Count(#temptable1.[TestResult]) As Inconclusive, Ip from #temptable1 
where [TestResult] = 'Inconclusive'
and ip = '10.1.1.1'
group by IP

select Count(#temptable1.[TestResult]) As Inconclusive, Ip from #temptable1 
where [TestResult] = 'Fail'
and ip = '10.1.1.1'
group by IP

select Count(#temptable1.[TestResult]) as TotalTests, Ip from #temptable1 
where ip = '10.254.180.202'
group by IP;
```

That'll give us a series of result tables showing Pass, Fail, and Inconclusive - but then we have a whole bunch of tables, rather than just one! In certain scenarios this will do just fine (and is perhaps easier to read than a pivot) but how can we aggregate these?

Well, we could brute force this now we have the select statements above:

```
Select (
select Count(#temptable1.[TestResult]) As Pass from #temptable1 
where [TestResult] = 'Pass'
and ip = '10.1.1.1'
group by IP ) as Passed,
(
select Count(#temptable1.[TestResult]) As Inconclusive from #temptable1 
where [TestResult] = 'Inconclusive'
and ip = '10.1.1.1'
group by IP) As Inconclusive,
(
select Count(#temptable1.[TestResult]) As Inconclusive from #temptable1 
where [TestResult] = 'Fail'
and ip = '10.1.1.1'
group by IP ) As Failed,
(
select Count(#temptable1.[TestResult]) as TotalTests from #temptable1 
where ip = '10.1.1.1'
group by IP) As Total
```

giving us

| **Passed** | **Inconclusive** | **Failed** | **Total** |
| --- | --- | --- | --- |
| 2 | 1 | 1 | 4 |

But that's seems like messy approach to our problem and not very scalable!

## The real pivot...

So let's define what how we want to summarise the data. In this case, let's say the below table is the result we'd like:

| **IP** | **Pass** | **Fail** | **Inconclusive** |
| --- | --- | --- | --- |
| **10.1.1.1** | 2 | 1 | 1 |
| **10.1.1.2** | 2 | 1 | 0 |

So we’ve PIVOTED the TestRESULT column and grouped by the IP address.

So we can start with a simple select statement laying out our table data including the **IP** column, the **TestResult** and a new column which we can **_SUM_** later (we’ll call this **_ResultSUM_**).

```
select *
from
(
  select IP, [TestResult], [TestResult] as ResultSUM -- The columns we want, plus a result we do our sum on
  from #temptable1
) src
```

But now we need to tell SQL what values we want and what the possible headers for our PIVOT will be and populate the values:

```
Count(ResultSUM) -- We have to do a count here
for [TestResult] in ([Failed], [Passed], [Inconclusive]) -- The possible PIVOT Headers
```

OK- that should be us. We need to tell SQL it’s a PIVOT too – so the final result should look something like this:

```
select *
from
(
  select IP, [TestResult], [TestResult] as Result -- The columns we want, plus a result we do our sum on
  from #temptable1
) src
pivot
(
  Count(ResultSUM) -- We have to do a count here
  for [Test State] in ([Failed], [Passed], [Inconclusive]) -- As the possible PIVOT Headers
) piv;
```

And that's it!
