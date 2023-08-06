#!/bin/bash
while true; do
	if [ ! "$(ps aux | grep x-relay  | grep -v grep )" ];then
		x-relay start
	else
		sleep 60
	fi
done