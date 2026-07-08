#!/bin/sh
exec socat TCP-LISTEN:16767,reuseaddr,fork EXEC:"timeout 60 /home/chal/chal",stderr
