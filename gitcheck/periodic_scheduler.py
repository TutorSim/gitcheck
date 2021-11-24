import contexts

from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *

from fetch import Fetch
from assess import Assess

from config import GoogleRosterConfig as grc
from init_semester import InitSemester as init


import pygsheets
config = grc(google_svc_key="./instance/gsvck.json", google_spread_data="SPREADSHEET_NAME", 
            git_id="GITHUB_ID", git_pw="GITHUB_PW",
            assessment_home="ASSESSMENT_HOME")

gc = pygsheets.authorize(service_file=config.get_google_svc_key())
sh = gc.open(config.get_google_spread_data())

init_semester = init()
student_list = init_semester.get_student_list(sh)

# System Simulator Initialization
se = SystemSimulator()
se.register_engine("sname", config.get_sim_mode(), config.get_time_density())

model = Fetch(0, Infinite, "fetch", "sname", student_list, 
              config.get_git_id(), config.get_git_pw(), config.get_assessment_home(),)

amodel = Assess(0, Infinite, "assess", "sname", config.get_assessment_home(),)

# engine에 입력포트를 추가
se.get_engine("sname").insert_input_port("start")

se.get_engine("sname").register_entity(model)
se.get_engine("sname").register_entity(amodel)

se.get_engine("sname").coupling_relation(None, "start", model, "start")
se.get_engine("sname").coupling_relation(model, "process", amodel, "student")

se.get_engine("sname").insert_external_event("start", None)
se.get_engine("sname").simulate()
