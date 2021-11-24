from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *

import os
import copy
import datetime
import subprocess as sp

class Fetch(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, student_list, git_id, git_pw, ahd):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 1)
        self.insert_state("WAIT", 86400*7)
        
        self.insert_input_port("start")
        self.insert_output_port("process")

        self.sl = student_list
        self.id = git_id
        self.pw = git_pw
        self.ahd = ahd
        self.process_list = []

    def ext_trans(self,port, msg):
        if port == "start":
            self._cur_state = "PROCESS"
            self.process_list = copy.deepcopy(self.sl)
    
    def output(self):
        #sdata = None
        msg = SysMessage(self.get_name(), "process")
        if self.process_list:
            student = self.process_list.pop()
            path, sdata = self.process_student(student)
            msg.insert(path)
            msg.insert(sdata)
        
        return msg
    
    def int_trans(self):
        if self.process_list:
            self._cur_state = "PROCESS"
        else:
            self._cur_state = "WAIT"
            self.process_list = copy.deepcopy(self.sl)

    def process_student(self, _student):
        # cwd: {ahd}/repositories/
        # check exist
        #  - init: mkdir _id
        #          change directory _id
        #          cwd: {ahd}/repositories/{_id}
        #          git clone
        #  - change directory _github
        #          cwd:{ahd}/repositories/{_id}/{_github}
        #          git pull
        #          git log ...
        #          write to assessment directory {ahd}/assessments/{date}/{_id}
        #  - cd ..
        _id = _student[0] # student[0] == ID
        _github = _student[1] # student[1] == github_id

        target_dir = f"{self.ahd}/repository/{_id}"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            os.chdir(target_dir)

            new_command = f"https://{self.id}:{self.pw}@github.com/HBNU-COME1101/practice-{_github}"
            
            sp.run(["git", "clone", new_command])
            os.chdir(f"{self.ahd}")


        try :
            os.chdir(f"{target_dir}/practice-{_github}")
            print(f"Processing {_id}'s commit logs")

            sp.run([ "git", "pull"])
            os.chdir("..")
        except OSError:
            pass

        return (f"{target_dir}/practice-{_github}", _student)