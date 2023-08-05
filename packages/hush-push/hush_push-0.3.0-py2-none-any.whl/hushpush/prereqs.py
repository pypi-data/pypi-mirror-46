import os

import git
import constant

def verify_config_file():
  if os.path.isfile(os.path.expanduser("~/.aws/config")):
    return True
  return os.getenv(constant.ENV_CONFIG_FILE_KEY) is not None

def verify_credentials_file():
  return os.path.isfile(os.path.expanduser('~/.aws/credentials'))

def verify_running_dir_is_git():
  cwd = os.getcwd()
  try:
    _ = git.Repo(cwd).git_dir
    return True
  except:
    return False
