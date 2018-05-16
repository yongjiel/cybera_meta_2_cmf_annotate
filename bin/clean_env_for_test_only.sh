#!/bin/sh
echo "rm /home/centos/Ana_projects/cfm_id/bin/*pyc"
for_each "rm /home/centos/Ana_projects/cfm_id/bin/*pyc"
echo "rm /home/centos/Ana_projects/cfm_id/log"
for_each "rm /home/centos/Ana_projects/cfm_id/log"
echo "rm /home/centos/Ana_projects/cfm_id/inputs/z_list_*"
for_each "rm /home/centos/Ana_projects/cfm_id/inputs/z_list_*"
echo "rm /home/centos/Ana_projects/cfm_id/cfmid/output/positive/*"
for_each "rm /home/centos/Ana_projects/cfm_id/cfmid/output/positive/*"
echo "rm  /home/centos/Ana_projects/cfm_id/outputs/positive/*"
rm  /home/centos/Ana_projects/cfm_id/outputs/positive/*
echo "for_each \"ps aux|grep cfm-ann|grep -v grep \""
for_each "ps aux|grep cfm-ann|grep -v grep " 
