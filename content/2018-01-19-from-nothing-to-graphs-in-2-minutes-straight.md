---
title: "From nothing to graphs in 2 minutes straight"
date: 2018-01-19
categories: 
  - "python"
tags: 
  - "data-visualisation"
  - "graphs"
---

I've only just started dipping my toes back into Python again after spending a long away (version 3 is a breath of fresh air!). In recent months it's felt as if I could hardly surf the web without hitting a wave of python examples showing you how to do something neat but looking for something simple yet rewarding to get started on wasn't quite as simple as I hoped.

So, after a bit of messing around (my preferred method of Rapid Development: Fail Until You Don't), I figured I'd share the steps to getting something nice out of Python that took me less than two minutes to setup. For now, we'll just generate a pretty looking graph based on random data, but hopefully you can see how you'd easily tweak this to run against any data you have handy...

NB: For my purposes I was using the rather neat functionality of Ubuntu on Windows 10 (which is a massive time saving in comparison to my ancient practice of installing an OS on a VM every time I wanted a terminal session to work with)- if you want to follow along you can simply setup the Ubuntu shell as per Microsoft's install guide (https://docs.microsoft.com/en-us/windows/wsl/install-win10) and once you're at the command prompt you're good to go:

1. Create a free account on ploty: [https://plot.ly/feed/](https://plot.ly/feed/)
2. Then get your API key: [https://plot.ly/settings/api](https://plot.ly/settings/api) (you’ll need to click regenerate a visible key)
3. Logon to your Ubuntu box and get the dependencies:

```
sudo apt-get install imagemagick libmagickcore-dev libmagickwand-dev libmagic-dev

sudo apt-get install imagemagick
```

4\. Install plotly:

```
sudo pip3 install plotly

pip3 install plotly –upgrade

# Used to generate random

pip3 install numpy
```

5\. Launch python and test you can draw stuff:

```
python3

import plotly

plotly.tools.set_credentials_file(username='yourusername', api_key='yourAPIkeyHere')

import plotly.plotly as py

import plotly.graph_objs as go

# Create random data with numpy

import numpy as np

N = 500

random_x = np.linspace(0, 1, N)

random_y = np.random.randn(N)

# Create a trace

trace = go.Scatter(

    x = random_x,

    y = random_y

)

data = [trace]

py.iplot(data, filename='basic-line')
```

and you’ll get yourself a link to your plotly online profile and a resulting pretty graph which is surprisingly pleasing.
