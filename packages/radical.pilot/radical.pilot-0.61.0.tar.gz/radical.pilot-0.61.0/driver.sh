#!/bin/sh

sleep 1
n=0
N=100
while test $n -lt $N
do
    uid=$(printf unit.%06d $n)
    mkdir /tmp/$uid/
    cp    unit.000000/unit.000000.sh /tmp/$uid/$uid.sh
    printf "EXEC $uid\n" >> /tmp/sh.1.pipe.in
    echo -n '.'
    n=$((n+1))
done

printf "EXIT bye\n\n" >> /tmp/sh.1.pipe.in
echo '#'
sleep 1

