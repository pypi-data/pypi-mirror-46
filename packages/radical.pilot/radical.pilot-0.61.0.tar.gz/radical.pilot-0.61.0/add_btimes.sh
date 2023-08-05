#!/bin/sh

sid=$1
test -z $sid && exit

cd $sid/pilot.0000
test -f bootstrap_0.prof && exit

echo "fix $sid"

t0=$(head -n 10 *.prof | grep -v '#time' |  grep ',' | sort -n | head -n 1 | cut -f 1 -d '.')
t1=$(tail -n 10 *.prof | grep -v '#time' |  grep ',' | sort -n | tail -n 1 | cut -f 1 -d '.')

cat > bootstrap_0.prof <<EOT
$t0,sync_abs,agent_0.bootstrap_0,MainThread,,,rivendell:127.0.0.1:1534453476.9891:1534453476.9891:sys
$t0,bootstrap_0_start,agent_0,MainThread,pilot.0000,,
$t1,bootstrap_0_stop,agent_0,MainThread,pilot.0000,,

EOT

