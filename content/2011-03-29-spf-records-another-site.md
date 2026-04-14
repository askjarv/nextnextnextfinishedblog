---
title: "SPF records (another site)"
date: 2011-03-29
tags: 
  - "dns"
  - "spf"
---

After my post the other day on SPF records, I would being doing a dis-service to everyone if I didn't post the equally groovy [http://www.microsoft.com/mscorp/safety/content/technologies/senderid/wizard/](http://www.microsoft.com/mscorp/safety/content/technologies/senderid/wizard/) - gives the same results, but explains a bit more about SPF records and the like.

Also, for those who are interested/want to know more, the wikipedia article on SPF is also great- [http://en.wikipedia.org/wiki/Sender\_Policy\_Framework](http://en.wikipedia.org/wiki/Sender_Policy_Framework) - and clarifies the difference's between +,  ~, and ? 's (you know, one of those difficult questions in life!)- from Wikipedia:

> ### Qualifiers
> 
> Each _mechanism_ can be combined with one of four _qualifiers_:
> 
> - **+** for a PASS result. This can be omitted; e.g., +mx is the same as mx.
> - **?** for a NEUTRAL result interpreted like NONE (no policy).
> - **~** for SOFTFAIL, a debugging aid between NEUTRAL and FAIL. Typically, messages that return a SOFTFAIL are accepted but tagged.
> - **\-** for FAIL, the mail should be rejected.
