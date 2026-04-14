---
title: "Building a habit tracking to-do app on Azure (part 2) - Design Thoughts"
date: 2019-01-04
---

Having decided on the platform I want to use yesterday and having a few ideas on possible approaches I started sketching out some rough ideas that I hoped would help me to build my app.

First off, I wanted to consider my inputs - effectively my to-do list tracker would need to track to-dos, but what details did I need to create to-do?

- An ID - something for the application internally to track, but probably something I'd expose in my early builds so I can test (deletions, insertions, etc)
- A name - this ideally should have a short name so it was easy to present graphically.
- A detailed description - this would
- A deadline date - unlike traditional don't break the chain style objectives, I also wanted to track shorter term habits and projects (something I couldn't see any other apps doing) - so I wanted to add an option deadline date.
- A start date/create date - this made sense since I had a deadline date, it meant I could track days on a task, as well as "missed days" over the period. I'd default it the date the task was created - I'm not too sure if I want to allow for user editing of this as it would complicate things!
- I wanted a category field (this would help me group and possibly assist with visualising tasks).
- A deleted field (another internal field for tracking if an entry is removed)
- A completed field (the final internal field, based on the progress of a task being marked as "closed-out")

Each day, I'd want to track progress on a to-do, so I wanted an update to include:

- Date of the update (so I can track the chain's entry).
- A notes field (to add any comments)
- Scheduled "next day" (to allow for weekend breaks, etc) _or_ a recurrence schedule (this might be easier from a user perspective to input for week day only tasks, etc). This would also be used to define a reminder for the task
- A "close-out"

I didn't want to overly complicate the input requirements (again, the name of the game was to keep user "friction" to a minimum). So with that "basic" data structure in place (when I'm planning my DB I expect to split some of this into separate tables for example, as well as whether or not the task was the best place to store the "next day" data) I was free to think about how best to "input" this data. I had a few options here:

1. A form - the most simple format - just each field set one after another, with the user able to move from field to field.
2. A chat style interface - effectively wrapping the form in a "back and forth" interaction - this had the benefit of being "pleasant" to work with, but perhaps didn't offer much flexibility and also may suffer from the issue that other "chat" apps suffer from by setting expectations of a more natural flow than chat bots can currently allow (especially in this case, since there's no real intelligence at play). One benefit this did offer though, was a static order and requirement list (no way to skip past a stage, and, since in almost all cases, I'd be wanted to force most fields to be filled in, this is pretty tempting).

Without wanting to turn this in to a bigger piece about HCI, it always surprises me that "data entry" has never really gotten much smarter. When I think of data entry there really are only a few options universal used:

1. Serial form entry -chat like interfaces, presenting only one field to fill in at a time, although some may allow for "hidden" responses (as seen in Google Assistant interactions for example)
2. Non-serial form entry - present the full form, allow the user to move around as need be, but typically expect it to be process from top to bottom, left to right.
3. Tabular data entry - presenting data entry fields "over a grid" as seen in Excel
4. Completely free-form - e.g. a graphics package's or Word Processor's data entry (especially with MS Word's ability to dynamically tab to the area a user might click to start data entry).
5. Navigable options - use space (move left, right, up, down, etc) to select a input options (as seen in Arcade game hi-score tables, etc).

It's interesting no other inputs have been discovered. Sure, we can wrap different UI's and metaphor's around these (and, some would rightly argue that the above options really are close to a spectrum rather than discrete input forms in many cases) but ultimately even cutting edge voice assistants still have the same communication bottlenecks for data input.

With this in mind, my plan is to start some mockups designs as my next step - I'll update shortly with my thoughts and design steps soon!
