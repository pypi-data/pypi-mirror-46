#!/usr/bin/env python
from colorama import Fore, Style, init
import sys
import prereqs
import constant
import argparse
import coloredlogs, logging
import boto3
import os
from paraminfo import ParamInfo
from terminaltables import AsciiTable
from botocore.exceptions import ClientError

init()

def init_logging(verbose=False):
  coloredlogs.install(level=[logging.INFO, logging.DEBUG][verbose], fmt="%(message)s")
  logging.debug("verbose mode enabled")


def verify():
  verification_status = {}
  verification_status["AWS config file found in environment or in homedir"] = prereqs.verify_config_file()
  verification_status["AWS credentials found in homedir"] = prereqs.verify_credentials_file()
  verification_status["current directory is a git repository"] = prereqs.verify_running_dir_is_git()

  for k in verification_status:
    if not verification_status[k]:
      raise Exception("prerequisite '%s' failed" % (k))
    logging.debug(k + ": " + (Fore.RED + "FAIL", Fore.GREEN + "OK")[verification_status[k]] + Style.RESET_ALL)

def version():
  print(constant.VERSION)


def get_profile_name(file):
  sarr = file.split("/")
  return sarr[1]

def get_key_value(file):
  sarr = file.split("/")
  return "/" + "/".join(sarr[2:])

def build_file_tree():
  cwd = os.getcwd() + "/secrets"
  logging.debug("current dir %s" % (cwd))
  file_tree = dict()
  files = []
  for r,d,f in os.walk(cwd):
    for file in f:
      if not ".secret" in file:
        full_path = os.path.join(r,file)
        p = ParamInfo(full_path)

        trimmed_file = full_path[len(cwd):]

        profile_name = p.profile
        if profile_name not in file_tree:
          file_tree[profile_name] = []
        file_tree[profile_name].append(p)

  return file_tree

def put_params(file_tree={},execute=False,overwrite=False,endpoint=None):
  headers = ["Profile","Parameter","Value","Overwrite","Status"]
  table_data = [headers]
  for profile in file_tree:
    client = boto3.Session(profile_name=profile).client("ssm", endpoint_url=endpoint)
    for param in file_tree[profile]:
      if execute:
        try:
          rsp = client.put_parameter(
            Name=param.param_name,
            Description='created by hush-push',
            Value=param.value,
            Type='SecureString',
            KeyId='alias/aws/ssm',
            Overwrite=overwrite
          )
          status = ("FAIL","OK")[rsp.get("ResponseMetadata").get("HTTPStatusCode") == 200]
          table_data.append([profile,param.param_name, param.value,overwrite,status])
        except ClientError as err:
          table_data.append([profile,param.param_name, param.value,overwrite,err.response["Error"]["Code"]])
      else:
        table_data.append([profile,param.param_name, param.value,overwrite,"DRY RUN"])

  table = AsciiTable(table_data)
  print(table.table)

parser = argparse.ArgumentParser(description="Hello world")
parser.add_argument("--version", action="version", version="hush-push %s" % (constant.VERSION), help="show the current version")
parser.add_argument("--execute", "-e", action="store_true", help="create the specified configuration parameters")
parser.add_argument("--overwrite", "-o", action="store_true", default=False, help="force put the configuration parameters even if they already exist")
parser.add_argument("--verbose", "-v", action="store_true", default=False, help="enable verbose logging")
parser.add_argument("--remote-endpoint", "-r", action="store", help="specify remote endpoint")


def main():
  args = parser.parse_args()
  init_logging(args.verbose)
  do_execute = args.execute
  do_overwrite = args.overwrite
  custom_endpoint = None

  if not do_execute:
    logging.info("dry run only, no configuration values will be changed on the remote")

  if args.remote_endpoint:
    logging.info("using endpoint %s" % (args.remote_endpoint))
    custom_endpoint = args.remote_endpoint

  try:
    verify()
  except Exception as error:
    logging.error(error)

  file_tree = build_file_tree()

  put_params(file_tree, do_execute, do_overwrite, custom_endpoint)

