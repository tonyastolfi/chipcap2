#!/bin/bash
while true; do
    python chipcap2.py | curl -H "Content-Type:application/json" -d @- https://dweet.io:443/dweet/for/ht77k-zero
    echo
    sleep 1
done