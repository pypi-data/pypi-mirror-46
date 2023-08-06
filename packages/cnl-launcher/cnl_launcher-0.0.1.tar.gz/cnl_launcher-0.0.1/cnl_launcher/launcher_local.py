import os
from multiprocessing.pool import ThreadPool
from random import randrange
from time import sleep
import sys

# Function to be executed in a thread
def launch_job(job_id):
    num_nodes = int(sys.argv[3])
    node_id = int(sys.argv[1])
    line_number = job_id*num_nodes + (node_id - 1)
    with open(sys.argv[2]) as fp:
        for i, line in enumerate(fp):
            if i == line_number:
                # execute line matching thread number
                print("node {}: found line {}".format(node_id,line_number))
                cmd = line.rstrip('\n')
                print("line is {}".format(cmd))
                os.system(cmd)
                break

def local():
    # Create job list for this node
    node_id = int(sys.argv[1])
    total_jobs = int(sys.argv[4])
    num_nodes = int(sys.argv[3])
    num_jobs = int(total_jobs / num_nodes)
    if (total_jobs % num_nodes >= node_id):
        num_jobs = num_jobs + 1
    job_id = list(range(0,num_jobs))

    # Instantiate a thread pool with 5 worker threads
    ppn = int(sys.argv[5])
    pool = ThreadPool(ppn)

    # Add the jobs in bulk to the thread pool
    pool.map(launch_job, job_id)

    #wait for jobs to finish
    pool.close()
    pool.terminate()

  
if __name__== "__main__":
    local()
