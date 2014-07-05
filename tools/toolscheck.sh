#!/bin/bash
###########################################################################################
#   This script should be list in crontab as below:
# */1 * * * * /home/haomatong/test/python/normaljs/tools/toolscheck.sh  > /dev/null 2>&1
###########################################################################################
DATASR=`date`
THEPATH="/home/otto/src/github/normaljs/tools/"
LOGFILE="updorderjson.log"

for procname in updorderjson.py
do
    #echo $procname
    INTERNUM=`ps ax | grep $procname | grep -v grep | grep  -v "defunct" | wc -l`
    if [ $INTERNUM -lt "1" ]
    then
        killall -9 $procname
        sleep 1
        (cd "${THEPATH}"; python ${THEPATH}${procname} >> ${THEPATH}${LOGFILE} 2>&1 &)
        echo "${procname} restart"$DATASR  >> ${THEPATH}/restart.log
    fi
done
