---
title: "Building a to-do app on Azure"
date: 2019-01-02
---

It's the new year and many of us are making new year's resolutions to do something new so I figured I'd try the same thing - starting with a new project to build a to-do list app that tracks and encourages my progress. Based on the (very popular at the moment) "don't break the chain" method (or, the [Seinfeld method](https://lifehacker.com/5886128/how-seinfelds-productivity-secret-fixed-my-procrastination-problem)) of making sure you always add an entry indicating that you're keeping on track (whether that's by doing something or not doing something is up to you), my intention is to build the app in the open, sharing my code, method, and thoughts as I go.

So, with that in mind, where did I start? Well a few decisions needed to be made:

- Platform(s): This one was easy - web. I hesitated for a brief moment, thinking about building an Android app (since I haven't built one in years) but then I remembered that for some of the things I wanted to track progress for (updating my blog for example!) I'd already be on my PC. A web app would give me the option of updating my to-do list on whatever platform I wanted, reducing friction which, I hoped, would encourage me (and other users) to stick with it.
- Back-end: I knew I wanted to use a "modern" DB (I've spent a lot of time working with MySQL and MS-SQL over the years, but rarely looked into newer options) - MongoDB looks like the winner at the moment. Node.JS was a no-brainer again for the same reason as MongoDB - a modern platform that would be useful to learn!
- Front-end: I wanted to use a modern web framework for my front end - again, I've been building websites for years, but rarely dove into the world of modern frameworks to simplify set up... at the moment Angular is looking highly likely as my choice (since it's often used in my day job too!).

With those out of the way (at least for now), I wanted to start thinking about what I wanted my app to be like. I know that the market place is already filled with similar ideas- some of which I liked, some of which I wasn't so keen on:

- I'd used [https://chains.cc/](https://chains.cc/) in the past, but eventually lost interest- it failed to keep my attention, and was clunky on mobile.
- Day by Day on Android ([https://play.google.com/store/apps/details?id=com.leoncvlt.daybyday](https://play.google.com/store/apps/details?id=com.leoncvlt.daybyday)) and found it effective, if rather simplistic. Unfortunately, one day it decided just to break, losing all my progress so I quit!
- Loop Habit Tracker - [https://play.google.com/store/apps/details?id=org.isoron.uhabits](https://play.google.com/store/apps/details?id=org.isoron.uhabits) - I'd seen, but not tried - this seems like a nice little app. It also made me think about creating a simple "widget" (or button press, perhaps using some puck.js I have lying around) to add to my tally easily.
- Habitica ([https://habitica.com/static/home](https://habitica.com/static/home)) also tempted me for a brief period - but was overly complicated for my liking - I wanted something that would be quick to enter data into and didn't require much thinking about- Habitica is definitely a neat solution, but not the right fit for me.
- Habitbull ([http://www.habitbull.com/](http://www.habitbull.com/)) also tempted me but failed to keep my interest for long - I knew I needed something more to keep my interest than just trying to keep my score close to 100 to motivate me.
- I also did a very quick google image search (!) for The Seinfeld method. I know this may appear like a some what random approach to market research, but a Google Image search sometimes lets you quickly spot novel approaches to the problem area that you hadn't considered before... but in this case, it largely revealed "manual methods" (paper versions) - I travel a lot, so big wall calendars don't do me much good (in fact, I've ended up making it an excuse not to engage with it), I'm not a big fan of potentially messy things (which I fear this would become) and... I want to build an app!

With that in mind, I had a couple of ideas in mind:

- A "chat based" app, that framed your daily entries as conversations with an encouraging "coach", sending you "messages" to see how you're getting on with a goal
- A more visual based approach, putting building blocks together to construct something in order to drive me to keep my progress going
- A game-ified style approach, that involved a simple narrative (to collect something, like spells, parts to a car engine, etc) that would reveal something new to me each day (and, in order to keep this interesting, it would have to reveal something I hadn't seen before)
- Or, as an alternative to the initial game-ified approach noted above, I debated a literal game portal, that unlocked new games or stories each day as a reward for completing jobs. This seemed like an impossible option to achieve (to build the content) until I realised I could "feed" it my Pocket Backlog, Amazon wishlist, itch.io wishlist, etc so I could literally reward myself for my work.

I liked all of these ideas so I decided my next step would be to sketch out what each would look like as hand-drawn prototypes tomorrow and see which appealed to me.
