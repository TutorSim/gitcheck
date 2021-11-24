class InitSemester():
    def __init__(self):
        pass

    def get_student_list(self, sh) :
        wks = sh.worksheet('title','fetch')
        df = wks.get_as_df()

        return df.values.tolist()