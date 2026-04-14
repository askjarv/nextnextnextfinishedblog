---
title: "Google's Unsigned APK Crackdown"
date: 2025-10-31
categories: 
  - "google"
tags: 
  - "android"
  - "opinion"
---

I'm late to publicly comment on this hot topic (and do my best not to post "opinions" online in general!), but I thought I'd offer a personal story on Google's moves to required app developers provide personal ID to back the signing of all apps that run on Android (for those who haven't read about this already, check out [https://www.androidauthority.com/android-sideload-offline-3598988/](https://www.androidauthority.com/android-sideload-offline-3598988/)).

Now I can see the argument for this - it makes sense to have a "responsible" person for applications so that there's someone to hold responsible if apps misbehave. Google specifically uses the "security angle" to explain their intentions:

> [Android's new developer verification is an extra layer of security that deters bad actors and makes it harder for them to spread harm.](https://developer.android.com/developer-verification)

But here's the thing - Google already has a pretty effective set of deterrents in place - by default:

- Google blocks external APKs, as well as vet apps that are published in the Google store (not very well, but that's a thought for another day),

- along with include controls to restrict excessive access (preventing some apps to work the way users would like)

- and warnings for end users (in the store, when launching the app, when using devices like cameras or mics).

On top of this, Google could've focus on better sandboxing, allowed users to switch to "secure Play store only apps" modes for their devices, implemented more advanced vetting for apps on the store, carved out more security requirements for third party app stores to allow for "apk re-distribution", etc, or a number of other options, but instead they've opted for this approach that puts the onus on developers and deprives users of [fantastic apps](https://f-droid.org/en/2025/09/29/google-developer-registration-decree.html). via stores like F-Droid.

## Why this feels a bit personal

I'm not a "big" Google app developer by any stretch - but last year I got back into making Android apps a bit more for what may seem like a rather weird reason.

On a perfectly normal day in the middle of the week, I started getting stomach pains (not tied to a rogue Android app!) and the next day went into hospital. I would stay there for over a week whilst I had an emergency surgical intervention and ended up having a [stoma](https://www.colostomyuk.org/information/what-is-a-stoma/).

It was a bit daunting waking up from surgery with a new thing to manage every day (plus recovering from the surgery in-of-itself) and during my recovery I had a bit of "adapting" to do - and one of the things I did during that down time was get to grips with Android development having not tinkered with the platform for a great many years (on old HTC phones if that gives you some sense of how far back we're talking!) and found it a really nice distraction.

With my health issue, I had a new objective to try this out again - I wanted an app to help me track my health in relation to the surgery. I wanted something private, focused on what _I_ needed, and not necessarily a generic app that put tips and tricks front and center or had onboarding workflows to drive "engagement". So I wrote my own (it's up on [Github](https://github.com/askjarv/stoma_tracker_app_android) if others want to have a look - be kind, as noted, I'm not a full time dev!).

That app has served me well - both from a directly practical perspective as well as from a mental health perspective - developing the app was a good distraction during a rough time. On top of that, having a privacy first app that I knew wasn't using my private medical data to make money, and yet cost nothing to use made me feel better - in fact, I'd say it gave me the piece of mind that I was on top of the ongoing health management and that was a form of relief that I'm not sure I would've found without it.

Now, I'd never sell this app (I think professional apps in the health field here would (rightly) require some deeper thinking about the implications of its use etc) but I am very grateful to be able to develop openly on Android and to have an app that I can run on my device that makes a difference to my life each and every day.

## The Wiggle room

Google isn't necessarily out to get me (and developers like me) to be fair. They've kindly carved out an exception for hobbyists like myself:

> We're committed to keeping Android an open platform for you to learn, experiment, and build for fun. We recognize that your needs are different from commercial developers, so we're working on a separate type of Android Developer Console account for you.

but not specified what will look like. That doesn't exactly reassure me, given it's another account with unspecified requirements, etc. It's obviously not a priority, either, given they haven't seemingly finalised what this looks like.

In addition to the hobbyist angle, Google has also (after some fuss seemingly) clarified that this won't impact ADB:

> [As a developer, you are free to install apps without verification with ADB](https://developer.android.com/developer-verification/guides/faq#:~:text=Will%20Android%20Debug,Sept%203%2C%202025)

but it remains unclear how they're balancing this "workaround" whilst maintaining their security goals (some have hinted at ties that might prevent such apps from working without internet access though that's reading between the lines - again, some certainty about Google's implementation here would help!).

Ultimately, both of these exceptions sound great, but without the details of the implementation, I just don't know if Android is the platform I'd want to tinker with anymore.

## What next

My interest in Android has always revolved around it's openness, even if I didn't always take advantage of it by building my own apps - I've instead benefited from others who have built apps outside of the Play Store that focus on privacy or utility that Google won't allow on their app store. I've embraced mobile devices as useful utilities because apps made it possible for millions to try out new pieces of software, but now I am definitely questioning whether mobile giants aren't exploiting their position to shape the world to their liking, not their users.

I'm all for improving the app ecosystem and security - but I don't think further gate keeping by Google is the way forward here. I've already implemented a web app version of my app - which I know Google will never know or care about, but if they were curious enough to talk to some tiny developers like myself perhaps they would come to know that such moves put off many developers for their ecosystem. I'm not here to get rich (which I guess means I also don't want to feed Google's coffers either) but I am keen to keep software development an activity a hobbyist can enjoy and even become successful from.

I know in this "big world" we often have to stop hobbyists from making things that they might enjoy (e.g. building their own car from scratch (that drives on the road) requires checks, as would a house, etc) but "open" software has shown the world that letting anyone pick up tools and share their results with the planet is a powerful opportunity to build a better world - perhaps this is one we should fight for this one.
