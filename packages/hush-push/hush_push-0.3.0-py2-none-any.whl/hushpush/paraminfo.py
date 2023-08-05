import os

class ParamInfo:
  value = ""
  profile = ""
  param_name = ""
  def __init__(self, file):
    f = open(file,"r")
    self.file = file
    self.value = f.read()
    f.close()
    self.calculate()

  def get_profile_name(self,file):
    sarr = file.split("/")
    return sarr[1]

  def get_key_value(self,file):
    sarr = file.split("/")
    return "/" + "/".join(sarr[2:])

  def calculate(self):
    trimmed_file = self.file[len(os.getcwd()+"/secrets"):]
    self.profile = self.get_profile_name(trimmed_file)
    self.param_name = self.get_key_value(trimmed_file)