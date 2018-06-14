vnimport - Playnite Plugin for Importing Visual Novel Metadata
=======
[Playnite](https://playnite.link/) is a open source video game library manager, like Steam. 
This plugin add the ability for Playnite to download visual novel metadata.

Motivation
============
Have you try to organize your visual novels collection not bought in Steam? 
You can definitely import those visual novels in Steam, or use a 3rd party game library like Playnite, 
but it is tedious to download metadata like developers, release date, cover image manually for better management.
This plugin can help you download those metadata automatically, and you can easily organize your visual novel collection, powered by Playnite.

Prerequisites
=============
* Installed Playnite. You can find installation instruction [here](https://github.com/JosefNemec/Playnite)

Installation
============
1. Download this [repository](https://github.com/wiktorduda/vnimport/archive/master.zip)
2. Inside the zip file, move `vnimport` folder to:
    1. If you are using installed version of Playnite: move `vnimport` folder to `C:\Users\%USERNAME%\AppData\Roaming\Playnite\IronPython`
    2. If you are using portable version of Playnite: move `vnimport` folder to `<basedir>\Scripts\IronPython`. 
        `<basedir>` is where your Playnite folder located.

Usage
=====
* In menu, click `Extensions` > `Download Metadata - vnimport`
    ![image](ext/usage-01.png "'Download Metadata - vnimport' menu")

FAQ
=====
### Why the plugin interface looks so bad?
* There are no styling options and only limited dialog from Playnite's API. 
    It is possible to have better interface if they update their API, but for the moment, it is the best I can provide.

### Where do I get those metadata?
* I get those data from API of [erogetrailers](http://ketsuage.seesaa.net/article/263754550.html). The API provide product ID of [Getchu.com](http://www.getchu.com). 
    Therefore, I can use the product ID to download cover image from [Getchu.com](http://www.getchu.com)

License
=======
BSD 3-Clause License

Copyright (c) 2018, Wiktor Duda
All rights reserved.