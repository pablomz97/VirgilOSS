#!/bin/bash

case $1 in
	screen)
		screen -L screenlog python3 src/bot.py 
		;;
	*)
		python3 src/bot.py
		;;
esac
