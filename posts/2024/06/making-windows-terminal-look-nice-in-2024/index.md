---
title: "Making Windows Terminal Look nice in 2024"
date: 2024-06-07
coverImage: "image.png"
---

I recently had to rebuild a PC recently and whilst a lot of my settings automatically came across (thanks OneDrive backup) my poor Windows Terminal did not do well with a profile migration. Setting up Windows in 2024 to work "nicely" with OH-MY-POSH (especially if your profile is a bit mangled by years of cruft and auto-sync'd rubbish) can be a bit more painful (particularly with some articles about Nerd font requirements, etc being scattered across various out-of-date articles) so I figured I'd document the process that worked for me!

First off, install your components:

- Install POSH itself:
    - [winget install JanDeDobbeleer.OhMyPosh -s winget](https://github.com/devblackops/Terminal-Icons?tab=readme-ov-file)

- Install PSReadLine
    - Install-Module PsReadLine -Force

- Pick your font:
    - oh-my-posh font install

Install Terminal Icons (for icons in ls/dir commands:)

- Add Terminal Icons:

- Do the fix indicated here: [https://gist.github.com/markwragg/6301bfcd56ce86c3de2bd7e2f09a8839](https://gist.github.com/markwragg/6301bfcd56ce86c3de2bd7e2f09a8839) - i.e.
    - Download and install this version of Literation Mono Nerd Font which has been specifically fixed to be recognized as monospace on Windows:
        - https://github.com/haasosaurus/nerd-fonts/blob/regen-mono-font-fix/patched-fonts/LiberationMono/complete/Literation%20Mono%20Nerd%20Font%20Complete%20Mono%20Windows%20Compatible.ttf
    
    - Modify the registry to add this to the list of fonts for terminal apps (cmd, powershell etc.):
        - $key = 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Console\\TrueTypeFont'
        
        - Set-ItemProperty -Path $key -Name '000' -Value 'LiberationMono NF'
    
    - Open PowerShell, right click the title bar > properties > Font > select your new font from the list.
    
    - Install and load Terminal-Icons:
        - Install-Module Terminal-Icons -Scope CurrentUser
        
        - Import-Module Terminal-Icons

[![](images/image.png)](https://nextnextnextfinished.wordpress.com/wp-content/uploads/2024/06/image.png)

In the end, my ($Profile) profile looks something like this;

oh-my-posh init pwsh | Invoke-Expression  
oh-my-posh init pwsh --config "$env:POSH\_THEMES\_PATH\\paradox.omp.json" | Invoke-Expression  
Set-TerminalIconsTheme

$ChocolateyProfile = "$env:ChocolateyInstall\\helpers\\chocolateyProfile.psm1"  
if (Test-Path($ChocolateyProfile)) {  
Import-Module "$ChocolateyProfile"  
}
