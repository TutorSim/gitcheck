from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *

import os
import copy
import datetime
import subprocess as sp

class Assess(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, ahd):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)
        
        self.insert_input_port("student")        
        self.ahd = ahd

        self.student_info = None

    def ext_trans(self,port, msg):
        if port == "student":
            self._cur_state = "PROCESS"
            self.student_info = msg.retrieve()
    
    def output(self):
        self.assess_student(self.student_info)
        return None
    
    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"

    def assess_student(self, info):

        try :
            os.chdir(info[0])
            _id = info[1][0]
            print(f"assessing {_id}'s commit logs")
            
            afterdate = datetime.datetime.today().date()
            beforedate =  afterdate + datetime.timedelta(days=-7)
            
            #sp.run('make') 파일 존재 안하면 0/  련타임에러 -> 0 / 출력 다르면 0 => 백준 느낌 / stdin => 표준입력, 변수값을 넣어주면 자동으로 입력 , 우와  재밌는 채점... parents class 처리... 상속... =>오버라이딩 그 998
            op_after = "--after='{0}'".format(beforedate.isoformat())
            op_before = "--before='{0}'".format(afterdate.isoformat())

            result = sp.run(['git', 'log', '--pretty=format:\'\"!!@@##%cn, %cd, %s\"\'', '--stat', op_after, op_before], stdout=sp.PIPE)

            assess_dir = f"{self.ahd}/asessment/{afterdate}"

            if not os.path.exists(assess_dir):
                os.makedirs(assess_dir)
            #모든학생들 로그가 만들어진다...

            
            if result.stdout != bytes(0) :    
                f = open(f"{assess_dir}/{_id}.log", "wb")
                print(result.stdout)
                f.write(result.stdout)
                f.close()
            os.chdir("..")
        except OSError:
            pass

            
        pass
