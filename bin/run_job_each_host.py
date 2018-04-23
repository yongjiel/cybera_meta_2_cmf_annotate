#!/usr/bin/python

# this program is for running cmfid docker image
# for output. It will use multiprocessing to make
# 2 threads to call cmfid docker image and get results
# cuncurrently until all the jobs done in input file.

import os
import sys
import config
from util import get_args, split_input_file
import re
import subprocess
from multiprocessing import Pool
import time

def jobs(argvs):
    input_file  = argvs[0]
    file_smile_dic = {}
    with open(input_file, "r") as f:   
        for line in f:
            basename = line.split("\t")[0]
            file = "{0}/{1}".format(config.input_files_dir, basename)
            file_smile_dic[file] = line.split("\t")[1].strip()
    category = argvs[2]
    der_arg = argvs[1]
    done_file = input_file + ".done"
    done_list = []
    if os.path.isfile(done_file):
        with open(done_file, 'r') as df:
            done_list = df.read().split("\n")
    #done_list = set(done_list)
    case_dir, dir_back_to_host, out_dir = get_standard_or_derivative_dirs(der_arg)

    for file in file_smile_dic.keys():
        smiles = file_smile_dic[file]
        if file in done_list:
            continue
        c = case_dir[category]
        remote_file = "{0}/{1}/{2}*".format(dir_back_to_host, c, os.path.basename(file))
        if check_exist_in_master_node(remote_file):
            print >> sys.stderr, "Bypass " + remote_file
            continue
        #print >> sys.stderr, "Run " + remote_file
        param_file, config_file = get_param_config_files(c)
        
        output_file, cmd, out, timeout = run_docker(file, out_dir, smiles, c, param_file, config_file)
        
        file_to_master_host = decide_file_to_master_node(output_file, der_arg, out_dir, basename, c, cmd, out, timeout)

        # transfer back to master host
        ok = scp_to_master_node(file_to_master_host, dir_back_to_host, c)
        
        #write done file
        if ok and not file in done_list:
            with open(done_file, "a") as df:
                df.write(file + "\n")

def get_standard_or_derivative_dirs(der_arg):
    ''' choose dirs when has derivative flag -d '''
    if not der_arg:
       case_dir = config.case_dir
       dir_back_to_host = config.dir_back_to_host
       out_dir = config.out_dir       
    else:
       case_dir = config.case_dir_d
       dir_back_to_host = config.dir_back_to_host_d
       out_dir = config.out_dir_d
    return case_dir, dir_back_to_host, out_dir



def scp_to_master_node(file_to_master_host, dir_back_to_host, c):
    cm = "scp {0} centos_1:{1}/{2}/.".format(file_to_master_host, dir_back_to_host, c)
    print cm
    sys.stdout.flush()
    cn =0
    p = ''
    while(cn < 5 ):
        p = subprocess.Popen(cm, stdout=subprocess.PIPE, \
            stderr=subprocess.STDOUT, shell=True)
        p.wait()
        cn += 1
    if not p.stderr:
        # delete the result file
        os.remove(file_to_master_host)
        return True
    else:
        print >> stderr, ",".join(p.stderr)
        return False



def decide_file_to_master_node(output_file, der_arg, out_dir, base_name, c, cmd, out, timeout):
    ''' if output_file is empty or not exist,
        error file will be generated. Then 
        the final file will be selected to go
        to master node.
    '''
    file_to_master_host = ''
    base_name = re.sub(r'\..*?$', '', base_name)
    # if failed, generate fail file
    if not os.path.isfile(output_file) or os.stat(output_file).st_size == 0:
        if not der_arg:
            fail_file = "{0}/{1}/{2}".format(out_dir, c, "{0}.fail".format(base_name))
        else:
            fail_file = "{0}/{1}/{2}".format(out_dir, c, "{0}_{1}_{2}.fail".format(base_name, 1, 1))
        with open(fail_file, "w") as ff:
            ff.write(cmd + "\n")
            if timeout == 0:
                ff.write("Time out {0} minutes!\n".format(config.timeout))
            else:
                ff.write(out.read() + "\n")
        file_to_master_host = fail_file
    else:
        file_to_master_host = output_file
    return file_to_master_host


def run_docker(file, out_dir, smiles, c, param_file, config_file):
    file = os.path.basename(file) 
    base_name = "{0}.log".format(file) 
    output_file = "{0}/{1}/{2}".format(out_dir, c, base_name)  
    cmd = ("docker run --rm=true -v {0}:/root " + " -v {1}:/root/files "
         "-i cfmid:latest sh -c \"cd /root/; cfm-annotate " +
         "'{2}' /root/files/{3} '' 10.0 0.01 {4} {5} {6}/{7};" +
         " chmod 777 /root/{6}/{7}; exit\" ").format(out_dir, config.input_files_dir, \
                smiles, file, param_file, config_file, c, base_name)
    print cmd
    sys.stdout.flush()
    x = config.timeout * 60 
    delay = 3
    timeout = int(x / delay)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, \
            stderr=subprocess.STDOUT, shell=True)
    while p.poll() is None and timeout > 0:
        time.sleep(delay)
        if os.path.isfile(output_file):
            timeout = 0
        else:
            timeout -= delay
    #p.wait()
    if timeout == 0:
        p.kill()
        # the above just kill 'docker run', the below will kill the exec in docker container.
        cmd = "ps aux|grep '.:.. cfm-'|grep {0}|tr -s ' '|cut -d ' ' -f 2|xargs sudo kill -9 ".format(file)
        p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, \
                stderr=subprocess.STDOUT, shell=True)  
        p1.wait()
    
    if os.path.isfile(output_file):
        print "{0} generated!".format(output_file)
        sys.stdout.flush()
    return output_file, cmd, p.stdout, timeout


def get_param_config_files(c):
    param_file = ''
    config_file = ''
    if c == 'positive':
        param_file = "/root/param_output0.log"
        config_file = "/root/param_config.txt"
    elif c == 'negative':
        param_file = "/root/negative_param_output0.log"
        config_file = "/root/negative_param_config.txt"
    elif c == 'ei':
        param_file = "/root/ei_param_output.log"
        config_file = "/root/ei_param_config.txt"
    return param_file, config_file


def check_exist_in_master_node(remote_file):
    cm1 = "ssh centos_1 \"ls {0}\"".format(remote_file)
    count = 0
    read_out = ''
    while(1):
        count += 1
        rp = subprocess.Popen(cm1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        rp.wait()
        read_out = rp.stdout.read()
        if read_out or count == 3:
            break
        time.sleep(3)
    return read_out

def run_jobs(input_file, pieces, der_arg, category):
    argvs = []
    for i in range(1, pieces+1):
        file = "{0}_{1}".format(input_file, i)
        argvs.append((file, der_arg, category))
    p = Pool(pieces)
    print argvs
    p.map(jobs, argvs)
    p.close()
    p.join()

def scp_files_into_child(input_file):
    # skip centos_1, no need to copy to itself.
    hostname = subprocess.check_output(["hostname"]).strip()
    if hostname == 'centos-1.novalocal':
        return
    files_list = []
    with open(input_file, 'r') as f:
        files_list = f.read().split("\n") 
    
    for line in files_list:
        file = line.split("\t")[0]
        cm = "scp centos_1:{0}/{1}  {0}/".format(config.input_files_dir, file)
        print cm
        sys.stdout.flush()
        cn =0
        while(cn <10 and not os.path.exists("{0}/{1}".format(config.input_files_dir, file))):
            p = subprocess.Popen(cm, stdout=subprocess.PIPE, \
               stderr=subprocess.STDOUT, shell=True)
            p.wait()
            cn += 1
        if not os.path.exists("{0}/{1}".format(config.input_files_dir, file)):
            print >> stderr, "Missing file {0}/{1}".format(config.input_files_dir, file)
            print "Program exit!!"
            exit(-1)

def main():
    der_arg, input_file, category = get_args("run_job_each_host.py")
    print "python ../bin/run_job_each_host.py {0} {1} {2}".format(input_file, category, der_arg)
    input_file  = "{0}/{1}".format(config.input_dir, os.path.basename(input_file)) 
    scp_files_into_child(input_file)
    pieces = split_input_file(input_file, config.pieces_in_each_host)
    print "Pieces {0}".format(pieces)
    run_jobs(input_file, pieces, der_arg, category)
    print "Program exit!"

if __name__ == "__main__":
   main()
