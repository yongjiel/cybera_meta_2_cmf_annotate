ls
cd ~
ld
ls
pwd
touch zz
cfmid-predict
which cfm-predict
cfm-predict
ls
rm zz
clear
ls
mkdir negative
cfm-predict "InChI=1S/C9H13NO2/c1-10-6-9(12)7-3-2-4-8(11)5-7/h2-5,9-12H,6H2,1H3/t9-/m0/s1" 0.001 /root/negative_param_output0.log /root/negative_param_config.txt 1 /root/negative/DB00388.log
ls
cd ei_param_
cd negative
ls
cat DB00388.log 
cd
exit
