#!/usr/bin/env python
import paramiko
import os
from os.path import abspath, exists
import argparse
import glob
import sys

PI_HOST = os.environ.get("PI_HOST")
PI_NAME = os.environ.get("PI_NAME")
PI_PASSWORD = os.environ.get("PI_PASSWORD")


class DeployClient():
    def __init__(self):
        
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
        self.ssh.connect(PI_HOST, username=PI_NAME, 
        password=PI_PASSWORD)
        
        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')


    #deploys rust project to pi for building and running
    def deploy(self, path):
        print('Deploying files...')
        self._upload(path)
        print('uploading done!')
        self.stdin.write('cd '+path + ' && cargo build && cargo run\n')
        self.stdin.flush()
        self._read_command()
        self.ssh.close()


    def _read_command(self):
        try: 
            for line in self.stdout:
                print(line)

        except KeyboardInterrupt:
            print('Shutting down gracefully...')
            pass


    def _upload(self, path):
        files = glob.glob(path+'**', recursive=True)
        for file in files:
            self._sftp(file)
         

    def _sftp(self, file):
        sftp = self.ssh.open_sftp()
        if os.path.isdir(file):            
            try: 
                sftp.mkdir(file)
            except IOError:
                pass
        else:
            sftp.put(file,file)
        sftp.close()


def print_help(**args):
    parser.print_help()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

list_parser = subparsers.add_parser("deploy", help="Deploys a project to pi")
list_parser.add_argument(
    "path", help="The entities to list")
list_parser.set_defaults(command="deploy")

if __name__ == "__main__":
    a = parser.parse_args()
    args = vars(a)
    print(args)
    command = args.pop("command", None)
    if not command:
        parser.print_help()
        exit(-1)
    client = DeployClient()
    getattr(client, command)(**args)        


