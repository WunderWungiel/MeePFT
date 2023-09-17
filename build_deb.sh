#!/bin/bash

blue='\033[96m'
red='\033[31m'
reset='\033[0m'
green='\033[32m'
blink='\033[5m'
yellow='\033[33m'
cyan='\033[1;36m'

set -e

rm -rf tmp *.deb
rm -rf lib/__pycache__

if ! command -v dpkg-deb > /dev/null 2>&1; then
    echo -e " $red"dpkg-dev not available..."$reset"
    exit 0
fi

if [[ -z $1 ]] || [[ $1 == "" ]]; then
    echo -e " $red"Provide version as argument..."$reset"
    exit 0
fi

mkdir tmp
cd tmp

mkdir -p {DEBIAN,usr/share,opt/MeePFT/bin}
mkdir -p usr/share/{icons/hicolor/80x80/apps,applications}

cat > usr/share/applications/MeePFT.desktop <<EOF
#!/usr/bin/env xdg-open
[Desktop Entry]
Type=Application
Name=MeePFT
Categories=System;
Exec=/usr/bin/invoker --splash=/opt/MeePFT/splash.png --type=e /usr/bin/meego-terminal -n -e /usr/bin/aegis-exec -s -u user -l "/opt/MeePFT/bin/MeePFT"
Icon=/usr/share/icons/hicolor/80x80/apps/MeePFT80.png
EOF

cat > opt/MeePFT/bin/MeePFT <<EOF
#!/bin/sh

cd /opt/MeePFT
./main.py
echo \$? > /tmp/meepft_status

if [ \$(cat "/tmp/meepft_status") -ne "0" ]; then
    echo "Please Enter to exit..."
    read
fi

exit 0
EOF

cat > opt/MeePFT/config <<EOF
[meepft]
port = 8000
dir = /
EOF

cp ../res/icon80.png usr/share/icons/hicolor/80x80/apps/MeePFT80.png
cp ../res/splash.png opt/MeePFT/

cp ../main.py opt/MeePFT
cp -r ../lib opt/MeePFT/

package="meepft"
version="$1"
arch="armel"
maintainer="Wunder Wungiel <me@wunderwungiel.pl>"
size=$(LANG=C du -c opt usr | grep total | awk '{print $1}')
depends="python-3.9.18-opt (= 3.9.18), viu-opt (= 1.4.0)"
section="user/system"
homepage="http://wunderwungiel.pl"
description="Python server wrapper, built upon Python"
display_name="MeePFT"

icon=$(base64 ../res/icon80.png)
icon2=""

IFS=$'\n'

for line in $icon; do
    icon2+=" $line\n"
done

cat > DEBIAN/control <<EOF
Package: $package
Version: $version
Architecture: $arch
Maintainer: $maintainer
Installed-Size: $size
Depends: $depends
Section: $section
Priority: optional
Homepage: $homepage
Description: $description
Aegis-Manifest: included
Maemo-Display-Name: $display_name
Maemo-Flags: visible
Maemo-Icon-26:
$icon2
EOF

rm -f ../md5
find -type f | grep -v "./DEBIAN" > ../md5
while read line; do if [ -f "$line" ]; then line=`echo "$line" | cut -c 3-`; md5sum "$line" >> DEBIAN/md5sums; echo S 15 com.nokia.maemo H 40 `sha1sum "$line" | cut -c -40` R `expr length "$line"` $line >> DEBIAN/digsigsums; fi; done < "../md5"
rm -f ../md5

cp ../control/* DEBIAN/

cd ..

filename="$package"_"$version"_"$arch".deb
dpkg-deb -b --root-owner-group -Zgzip tmp/ $filename > /dev/null

ar r "$filename" _aegis

rm -rf tmp

echo -e "$green"Package "$package" created. Output: "$cyan""$filename""$reset"
