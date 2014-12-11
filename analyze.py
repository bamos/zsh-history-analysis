#!/usr/bin/env python3

import argparse
import os
import sys
import time

class Command:
    def __init__(self,raw):
      tup = raw.split(";")
      self.timestamp_epoch = int(tup[0][2:-2]) # TODO: Should this be hard-coded?
      self.timestamp_struct = time.gmtime(self.timestamp_epoch)
      self.full_command = tup[1]
      self.base_command = tup[1].split()[0]

class HistoryData:
    def __init__(self,filename):
        with open(filename,'rb') as f:
            commands = []
            it = iter(f)
            for line in it:
                try:
                    full_line = line.decode()
                    while full_line.strip()[-1] == '\\':
                        full_line += next(it).decode()
                    commands.append(Command(full_line))
                except Exception as e:
                    #print("Warning: Exception parsing.") # TODO
                    #print(e)
                    pass
            self.commands=commands

    def get_times_hour(self):
        return [cmd.timestamp_struct.tm_hour for cmd in self.commands]

    def get_times_wday(self):
        return [cmd.timestamp_struct.tm_wday for cmd in self.commands]

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--history-dir',type=str,default="data")
    parser.add_argument('--analysis-dir',type=str,default="analysis")
    parser.add_argument('--plots-dir',type=str,default="plots")

    subparsers = parser.add_subparsers(help='sub-command help',dest='cmd')
    subparsers.required = True
    parser_timeFrequencies = subparsers.add_parser('timeFrequencies')

    args = parser.parse_args()

    def mkdir_p(path):
        try: os.makedirs(path)
        except: pass
    mkdir_p(args.analysis_dir)
    mkdir_p(args.plots_dir)

    all_history = []
    for filename in os.listdir(args.history_dir):
        all_history.append(HistoryData(args.history_dir+"/"+filename))

    if args.cmd == 'timeFrequencies':
        hours = []
        for history in all_history:
            hours += history.get_times_hour()
        with open(args.analysis_dir+"/time-hours.csv","w") as f:
            f.write(",".join([str(h) for h in hours])+"\n")

        wdays = []
        for history in all_history:
            wdays += history.get_times_wday()
        with open(args.analysis_dir+"/time-wdays.csv","w") as f:
            f.write(",".join([str(wd) for wd in wdays])+"\n")
