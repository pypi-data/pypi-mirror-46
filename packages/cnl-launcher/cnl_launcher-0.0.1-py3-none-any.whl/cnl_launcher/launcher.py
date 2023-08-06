import os
from fabric import Connection
from multiprocessing.pool import ThreadPool
import paramiko
import threading
import subprocess

def connect_to_hosts(host):
    for i in range(100):
        try:
            thread_name = threading.current_thread().getName()
            print("current thread name is {}".format(thread_name))
            thread_number = thread_name.split('-')[1]
            cmd_string = 'python3 ' + os.environ["CNL_LAUNCHER_DIR"] + '/cnl_launcher/launcher_local.py ' + thread_number + ' ' + os.environ["LAUNCHER_JOB_FILE"] + ' ' + os.environ["SLURM_NNODES"] + ' ' + os.environ["LAUNCHER_NJOBS"] + ' ' + os.environ["LAUNCHER_PPN"]
            result = Connection(host).run(cmd_string)

            print("{}: {}: exit {}".format(host, result.stdout.strip(), result.exited))
            break
        except paramiko.ssh_exception.AuthenticationException:
            print("Connection to {} failed. Trying again.".format(host))
            if (i == 100):
                print("No more tries. Connection failed.")


def main():
    # split slurm nodelist to populate hostenames list
    slurm_nodelist = os.environ["SLURM_NODELIST"]
    slurm_nodelist = slurm_nodelist.rstrip(']')	#remove last bracket
    slurm_nodelist = slurm_nodelist.split('],')	#split groups with different hostname bases
    hostlist = []
    for node_group in slurm_nodelist:
        nodelist = node_group.split('[')
        hostname = nodelist[0]
        nodelist = nodelist[1].split(',')
        for i in nodelist:
            node_range = i.split('-')
            if len(node_range) == 1:
                hostlist.append(hostname + node_range[0])
            else:
                for i in range(int(node_range[0]), int(node_range[1]) + 1):
                    hostlist.append(hostname + str(i))
    #print(hostlist)

    # set launcher environment variables
    #TODO: add other launcher environment variables here
    with open(os.environ["LAUNCHER_JOB_FILE"]) as f:
        for i, l in enumerate(f):
            pass
    num_jobs = i + 1
    os.environ['LAUNCHER_NJOBS'] = str(num_jobs)
    if "LAUNCHER_PPN" in os.environ:
        pass # keep value set by user
    else:
        os.environ['LAUNCHER_PPN'] = 24   # default to 24 (max for hikari)

    #ssh to all the hosts in parallel and run jobs
    print("number of nodes is {}".format(int(os.environ["SLURM_NNODES"])))
    print("job file is located at {}".format(os.environ["LAUNCHER_JOB_FILE"]))
    print("number of jobs is {}".format(int(os.environ["LAUNCHER_NJOBS"])))
    print("number of processes per node is {}".format(int(os.environ["LAUNCHER_PPN"])))

    pool = ThreadPool(int(os.environ["SLURM_NNODES"]))

    # Add jobs to the thread pool
    pool.map(connect_to_hosts, hostlist)

    #wait for jobs to finish
    pool.close()
    pool.terminate()

  
if __name__== "__main__":
    main()
