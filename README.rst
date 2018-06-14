vnimport - Playnite Plugin for Importing Visual Novel Metadata
=======
This plugin add the ability for Playnite_ to download visual novel metadata automatically.

.. _Playnite: https://playnite.link/

Motivation
============
Have you try to organize your visual novels collection not bought in Steam_? 

You can definitely import those visual novels in Steam_, or use a 3rd party game library like Playnite_, 
but it is tedious to download metadata like developers, release date, cover image manually for better management.

This plugin can help you download those metadata automatically, and you can easily organize your visual novel collection, 
powered by Playnite_.

.. _Steam: https://store.steampowered.com/

Prerequisites
=============
* Installed Playnite_. You can find installation instruction here_.

.. _here: https://github.com/JosefNemec/Playnite

Installation
============
1. Download this repository_.
2. Inside the zip file, move :code:`vnimport` folder to:

   1. If you are using installed version of Playnite: move :code:`vnimport` folder to :code:`C:\Users\%USERNAME%\AppData\Roaming\Playnite\IronPython`
   2. If you are using portable version of Playnite: move `vnimport` folder to :code:`<basedir>\Scripts\IronPython`. :code:`<basedir>` is where your Playnite folder located.
        
.. _repository: https://github.com/wiktorduda/vnimport/archive/master.zip

Usage
=====
* In menu, click :code:`Extensions` > :code:`Download Metadata - vnimport`
* .. image:: /ext/usage-01.png
           :alt: 'Download Metadata - vnimport' menu

FAQ
=====

Why the plugin interface looks so bad?
----

* There are no styling options and only limited dialog from Playnite_'s API. It is possible to have better interface if they update their API, but for the moment, it is the best I can provide.

Where do I get those metadata?
-----

* Those data are from API of erogetrailers_. The API provide product ID of Getchu.com_. Therefore, I can use the product ID to download cover image from Getchu.com_

.. _erogetrailers: http://ketsuage.seesaa.net/article/263754550.html
.. _Getchu.com: http://www.getchu.com

License
=======
BSD 3-Clause License

Copyright © 2018, Wiktor Duda
All rights reserved.
