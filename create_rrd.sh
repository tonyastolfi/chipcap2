#!/bin/bash
rrdtool create rh_temp.rrd \
    --start now \
    --step 5 \
    DS:rh:GAUGE:10:0:100 \
    DS:tempF:GAUGE:10:0:212 \
    RRA:AVERAGE:0.5:12:60 \
    RRA:AVERAGE:0.5:720:24 \
    RRA:MIN:0.5:720:24 \
    RRA:MAX:0.5:720:24
