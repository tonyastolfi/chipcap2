#!/usr/bin/env bash
if [ "$1" == "" ]; then
    echo "usage: install.sh REPORTING_LOCATION"
    exit 1
fi

srcdir=$(cd $(dirname $0) && pwd)
cp -f $srcdir/init-d-chipcap2 /etc/init.d/chipcap2
sed -i -e "s,CHIPCAP2_SOURCE_DIR,${srcdir},g" /etc/init.d/chipcap2
sed -i -e "s,CHIPCAP2_REPORTING_LOCATION,${1},g" /etc/init.d/chipcap2
chmod +x /etc/init.d/chipcap2
rm -f /etc/rc3.d/chipcap2
ln -s /etc/init.d/chipcap2 /etc/rc3.d/S06chipcap2
