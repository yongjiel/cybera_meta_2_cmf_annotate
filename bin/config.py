#!/user/bin/python

pieces = 15  # split files into these pieces
pieces_in_each_host = 2 #split input file into these pieces in each host
root = "/home/centos/Ana_projects/cfm_id" # root of project
out_dir = "{0}/cfmid/output".format(root)  # dir where to store the output of docker image
case_dir = {'-e': "ei",
            '-n': "negative",
            '-p': "positive"} # the specific case output dirs for each image run. If you do not want some of them, just change this list.
dir_back_to_host = "/mnt/one/Ana_projects/results"  # dir of the result file back to master host
timeout = 40 # minutes for time out of docker run
###
###If call the program with -d arg, the below vars will be used instead of upper vars.
###
case_dir_d = {'-e': "ei",
            '-n': "negative",
            '-p': "positive"} # the specific case output dirs for each image run. If you do not want some of them, just change this list. for derivatives.
dir_back_to_host_d = "/mnt/one/Ana_projects/results_d"  # dir of the result file back to master host. for derivatives.
out_dir_d = "{0}/cfmid/output_d".format(root)  # dir where to store the output of docker image, for derivatives.
log_file = "{0}/log".format(root) # all childs will log the run_job_each_host.py program.
input_files_dir = "{0}/inputs/files".format(root) # location of spectra txt files.
input_dir = "{0}/inputs".format(root) # input summary files location
bin_dir = "{0}/bin".format(root) # bin dir of project
