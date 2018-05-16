#!/usr/bin/python

# this program is used to split input files into pieces
# and then dispatch them to each host to start their jobs.
# The result will be transferred back to the master host 
# in each node's jobs.

import sys
import os
import config
import subprocess
from multiprocessing import Pool
from util import get_args, split_input_file

def transfer(argvs):
    ''' no need to transfer files to master node.'''
    file = argvs[0] 
    i_piece = argvs[1]
    host = "centos_{0}".format(i_piece)
    if host == 'centos_1':
        return
    cmd = "scp {0} {1}:{2}/.".format(file, host, config.input_dir)
    print cmd
    os.system(cmd)
    
def transfer_files(input_file, pieces):
    argvs = []
    for i in range(1, pieces+1):
        file = "{0}_{1}".format(input_file, i)
        argvs.append((file, i))
    p = Pool(pieces)
    p.map(transfer, argvs)
    p.close()
    p.join()

def run_cmd(argvs):
    file = argvs[0]
    i_piece = argvs[1]
    der_arg = argvs[2]
    category = argvs[3]
    host = "centos_{0}".format(i_piece)
    file = os.path.basename(file)
    cmd = "ssh {0} \"python {1}/run_job_each_host.py {2}/{3} {4} {5} > {6} 2>&1 \" ".format(host, config.bin_dir, config.input_dir, file, category, der_arg, config.log_file)
    print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, \
                        stderr=subprocess.STDOUT, shell=True)
    p.wait()

def run_remote_cmd(input_file, pieces, der_arg, category):
    argvs = []
    for i in range(1, pieces+1):
        file = "{0}_{1}".format(input_file, i)
        argvs.append((file, i, der_arg, category))
    p = Pool(pieces)
    p.map(run_cmd, argvs)
    p.close()
    p.join()

def send_jobs(input_file, pieces, der_arg, category):
    transfer_files(input_file, pieces)
    print "Transferring input summary files done!"
    run_remote_cmd(input_file, pieces, der_arg, category)
    print "Running remote run_job_each_host.py......"

def main():
    der_arg, input_file, category = get_args("send_jobs.py")
    print "python ../bin/send_jobs.py {0} {1} {2}".format(input_file, category, der_arg)
    input_file  = "{0}/{1}".format(config.input_dir, os.path.basename(input_file)) 
    pieces = split_input_file(input_file, config.pieces)
    send_jobs(input_file, pieces, der_arg, category)
    print "Program exit!"

if __name__ == "__main__":
   main()
 
