 
import sys
import os
import os
import re
import threading
import json


def setup(home_folder, config_file):
    workdir = input('Please input the ssh job workdir\n')
    with open(os.path.join(home_folder,config_file),'w') as fp:
        fp.write(workdir)
        print(workdir)
    


# def ssh_task():
#     from gcr import GCR


#     a = GCR()

#     while True:
#         print('\n#####################start####################################\n')
#         print(a.cluster_all)
#         cluster = input('\nplease in put the cluster id:\n')
#         if cluster=='clear':
#             continue
#         else:
#             cluster = int(cluster)
#         a.load_from_json(cluster=cluster)
#         while True:
#             print(a.nice)
#             task_id = input('\nplease input the ssh task id\n')
#             if task_id == 'clear':
#                 break
#             else:
#                 task_id = int(task_id)
#             a.ssh(task_id)
        


def ssh():
    if len(sys.argv) > 2:
        name = sys.argv
    elif len(sys.argv)==2:
        name = sys.argv[1]
    elif len(sys.argv)==1:
        name = 'yue wang'


    print("hello {}!".format(name))

    home_folder = os.environ['USERPROFILE']
    config_file = '.gcrssh.config'

    if os.path.exists(os.path.join(home_folder,config_file)):
        with open(os.path.join(home_folder,config_file)) as fp:
            workdir = fp.readlines()

    else:
        setup(home_folder, config_file)
        with open(os.path.join(home_folder,config_file)) as fp:
            workdir = fp.readlines()

    workdir = workdir[0]

    os.chdir(workdir)
    sys.path.append(workdir)
 

    os.system('python ssh_task.py')


 