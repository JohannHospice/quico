#!/usr/bin/env python3
import argparse
import subprocess

def main():
    args, unknown_joined = parse_known_args()
    
    build_cmd = CommandBuilder(['docker', 'build'])
    build_cmd.append_with_option('-f', args.file)
    build_cmd.append_with_option('-t', args.tag)
    build_cmd.append(args.directory)
    
    run_cmd = CommandBuilder(['docker', 'run'])
    run_cmd.append_with_option('--network', args.network)
    for volume in args.volume if args.volume else []:
        run_cmd.append_with_option('-v', volume)
    run_cmd.append_with_option('-p', args.publish)
    run_cmd.append_with_option('-ti', args.tag)
    run_cmd.append(unknown_joined)

    try :
        read_proc('build', build_cmd.build())
        read_proc('run', run_cmd.build())
    except Exception as e:
        print(e)

def parse_known_args():
    parser = argparse.ArgumentParser(description='Quico ou quick-container permet de compiler puis lancer rapidement un conteneur docker.')
    parser.add_argument('directory', help='Dossier ou compiler l\'image docker.')
    parser.add_argument('-t', '--tag', required=True)
    parser.add_argument('-n', '--network', help="Réseau ou lancer le conteneur docker", default='bridge', required=False)
    parser.add_argument('-f', '--file', help="Chemin vers le Dockerfile à compiler", default='Dockerfile', required=False)
    parser.add_argument('-p', '--publish', required=False)
    parser.add_argument('-v', '--volume', action='append', required=False)
    
    args, unknown =  parser.parse_known_args()
    unknown_joined = ' '.join(unknown)
    
    return args, unknown_joined

def read_proc(title, cmd):
    print(f"+{title}: start ({cmd})")
    try:
        subprocess.check_call(cmd, shell=True)
    except:
        raise Exception(f"+{title}: raised error")

class CommandBuilder:
    cmd = []

    def __init__(self, cmd):
        self.cmd = cmd

    def append_with_option(self, option, value):
        if value:
            self.cmd.append(option)
            self.cmd.append(value)
        return self

    def append(self, text):
        self.cmd.append(text)
        return self

    def build(self):
        return " ".join(self.cmd)


if __name__ == '__main__':
    main()
