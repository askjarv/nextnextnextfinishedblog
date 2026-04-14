---
title: "Free transfer of playlists from Google Play Music to Spotify..."
date: 2018-02-12
---

After a lot of soul searching, I decide that I would try out Spotify after being a long term Google Play Music user. My motivation was simple- I was being mocked for my Amazon Echo's playlist being absolutely awful! Since most of my music lived in Google Play Music and there's no support (and unlikely to be given Amazon's recent tiffs with Google) for Alexa controlled playback, I figured I'd tried the other big player (and no, that's definitely not Amazon Music!).

I figured it would be possible to move my playlists, thumbs up-ed tracks easily enough but Google are kind enough to make selecting all the items on a playlist not possible so I started a web hunt... and found I'd have to pay for the pleasure. I don't mind this as a business, but since I only have 200-300 items in total paying £10 pound (or more!) to move this seemed a bit over kill - especially since it would be a single run operation. Fortunately I did find a way:

Starting with gmusic-playlist.js

1. Grab chrome: tampermonkey extension
2. Open the gmusic-playlist.user.js script in your browser and click the install button (https://github.com/soulfx/gmusic-playlist.js/)
3. Open Google Play Music and click on the menu (top left)
4. Chose Export Playlists to generate a CSV...

Then use Playlist Convertor...

1. Take your CSV file and import it to http://www.playlist-converter.net/#/
2. Press convert and, once authorised, your playlists will be built

Easy enough with the right tools!
