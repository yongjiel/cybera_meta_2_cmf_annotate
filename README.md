# cfmid_cybera_cloud
This project is to run cfmid docker images in cybera_cloud to yield thousands of results.

0. Before run program, take care of bin/config.py first. Change it if
   necessary.

1. tsv_file can contain multiple columns, the first one must be ID name,
  the second one must be inchi or smiles. The third one or more are not 
  the matter. They must be tab delimited.
  For example, ~/cfm_id/inputs/list_2.0.

1.1 For derivatives,  tsv file must contain 4 columns. First is HMDB_ID,
   second is the derivative groups count, the third is unique number for 
   the same of HMDB_ID and derivative group count. THis 3 columns will be
   used to defind the output filename. The fourth column is smiles.

2. How to run:
  cd ~/cfm_id/inputs/;nohup python ../bin/send_jobs.py  <tsv file>
  For example, nohup python ../bin/send_jobs.py list_2.0
  For derivatives, nohup python ../bin/send_jobs.py test.tsv -d

3. ~/cfm_id/outputs is a link to /mnt/one/results. So 
  take care of it. For derivatives,  ~/cfm_id/outputs_d is a link to
  /mnt/one/results_d.

4. To stop the all jobs in cloud, run 
  cd ~/cfm_di/bin; ./stop_jobs.sh
