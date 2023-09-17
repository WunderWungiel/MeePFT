# MeePFT
(**Mee**Go **P**ython **F**ile **T**ransfer)

**MeePFT** is a primitive, yet working Python HTTP server runner for Nokia N9 / N950 devices running MeeGo Harmattan.

## Installing

You need to have [Developer Mode](http://wunderwungiel.pl/MeeGo/posts/devmode-22.04.2023.html) enabled and [Aegis-hack](https://talk.maemo.org/showthread.php?t=90750).
Python needs to be installed. Download Optified PATH, OpenSSL 1.1.0h and Python 3.9.18:

http://wunderwungiel.pl/MeeGo/apt-repo/pool/testing/python-3.9.18-opt_3.9.18_armel.deb
http://wunderwungiel.pl/MeeGo/apt-repo/pool/testing/optified-path_0.0.2_armel.deb
http://wunderwungiel.pl/MeeGo/apt-repo/pool/testing/openssl-opt_1.1.0h_armel.deb

Put in MyDocs.
Run **Terminal**, and type following commands:

    devel-su
    (enter "rootme" without quotes as password)
    cd /home/user/MyDocs
    aegis-dpkg -i python-3.9.18-opt_3.9.18_armel.deb optified-path_0.0.2_armel.deb openssl-opt_1.1.0h_armel.deb

Download latest release (`.deb` file) from [Releases](https://github.com/WunderWungiel/MeePFT/releases) page, and transfer it to N9, saving in **MyDocs** (i.e. **Nokia N9** drive when connected to PC).
Run the **Terminal** again, and type following commands:

    devel-su
    (enter "rootme" without quotes as password)
    cd /home/user/MyDocs
    aegis-dpkg -i meepft_RELEASE_armel.deb
    (replace RELEASE with the proper number, i.e. 0.0.1)
If you don't see any errors, you're ready to use MeePFT.

## How to use

**MeePFT** is a **CLI** app with no native **GUI**. However, it has been designed to make the usage as easy as possible! You don't need to enter any commands.
Just **run MeePFT** from applications menu while being connected to Wi-Fi. You will see a retro-style menu with few options, like **Start**. Below is a quick description of functions.

Each function will ask you for something - select option using **arrows**, and confirm using **Enter**. Sometimes you need to enter your "answer" and press **Enter** to confirm.

## Packaging MeePFT yourself

You can package MeePFT yourself! Just run `build_deb.sh` script in current directory. A MeePFT DEB will appear in few seconds, ready to be installed. Note: using nightly branch is unrecommended, because it containts latest, developed right now and not properly tested functions!

## Credits

 - [IarChep / Ярослав](https://t.me/iaroslavchep) - icon, splash
 - [Python](https://python.org) for making an easy to learn, power programming language.
