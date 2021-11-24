class Config():
    def __init__(self, sim_mode='REAL_TIME', 
                       time_density=1,
                       assessment_home="",
                       git_id="",
                       git_pw=""):
        
        self.sim_mode = sim_mode
        self.time_density = time_density
        self.assessment_home = assessment_home
        self.git_id = git_id
        self.git_pw = git_pw

    def get_sim_mode(self):
        return self.sim_mode

    def get_time_density(self):
        return self.time_density

    def get_assessment_home(self):
        return self.assessment_home

    def get_git_id(self):
        return self.git_id
    
    def get_git_pw(self):
        return self.git_pw

class GoogleRosterConfig(Config):
    def __init__(self, sim_mode='REAL_TIME', 
                       time_density=1,
                       assessment_home="~/classroom",
                       telegram_key="",
                       google_svc_key="",
                       google_spread_data=None,
                       git_id="",
                       git_pw=""):

        Config.__init__(self, sim_mode, time_density, assessment_home, git_id, git_pw)
        
        self.telegram_key = telegram_key
        self.google_svc_key = google_svc_key
        self.google_spread_data = google_spread_data
        
    def get_telegram_key(self):
        return self.telegram_key

    def get_google_svc_key(self):
        return self.google_svc_key

    def get_google_spread_data(self):
        return self.google_spread_data
    pass