#!/bin/bash
# this script only runs in master node centos_1
echo "===Kill the send_jobs.py in master node==="
ps axu|grep send_jobs|tr -s ' '|cut -d ' ' -f 2|xargs -I {} kill -9 {} 
echo "===Kill run_job_each_host.py jobs first===" 
for_each "ps aux|grep run_|grep -v grep|tr -s ' '|cut -d ' ' -f 2|xargs -I {} kill -9 {}"
echo "===Stop docker jobs cfm-predict==="
for_each "ps aux|grep '.:.. cfm-'|tr -s ' '|cut -d ' ' -f 2|xargs -I {} sudo kill -9 {}"
echo "==== Remove docker containers ====="
for_each "docker ps -a|grep 'cfmid'|tr -s ' '|cut -d ' ' -f 1|xargs -I {} docker rm -f {} " 
