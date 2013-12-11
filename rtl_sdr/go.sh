#!/bin/bash
# ------ RADIOGRAPHIE -----
# -- script de lancement --
# -- cecile beau ----------
# -- nicolas montgermont --
# -- v 0.1 / 2012 ---------
cd Dropbox/radiographie/patch/v13
echo "////////////////////// LAUNCH GNURADIO"
python sdr2pd.py &
PIDPYTHON=$!
sleep 5
echo "////////////////////// LAUNCH GNURADIO OK PID: $PIDPYTHON"
sleep 0.2
echo "////////////////////// LAUNCH PD"
pd -nomidi -rt -nosleep -alsa _main.pd & 
PIDPD=$!
echo "////////////////////// LAUNCH PD OK PID: $PIDPD"
while [ true ]
do
	if [ ! -d /proc/$PIDPYTHON ]
	then
		echo "////////////////////// gnuradio down, relance gnuradio"
		python sdr2pd.py &
		sleep 5
		PIDPYTHON=$!
		sleep 1
	fi
	if [ ! -d /proc/$PIDPD ]
	then
		echo "////////////////////// pd down, relance pd"
		killall pd
		pd -nomidi -rt -nosleep -alsa _main.pd & 
		PIDPD=$!
		sleep 1
	fi
sleep 1
done
