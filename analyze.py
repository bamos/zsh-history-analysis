#!/usr/bin/env python3

import argparse
import os
import sys
import time
from itertools import groupby
from collections import Counter,defaultdict
import statistics

def groupByKey(m):
    groupedM = defaultdict(list)
    for k,v in m:
        groupedM[k].append(v)
    return groupedM

class Command:
    def __init__(self,raw):
      tup = raw.split(";")
      self.timestamp_epoch = int(tup[0][2:-2]) # TODO: Should this be hard-coded?
      self.timestamp_struct = time.gmtime(self.timestamp_epoch)
      self.full_command = tup[1]
      self.base_command = tup[1].split()[0]

class HistoryData:
    def __init__(self,filenames):
        if isinstance(filenames,str):
            filenames = [filenames]
        commands = []
        for filename in filenames:
            with open(filename,'rb') as f:
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

    def get_hourly_breakdowns(self):
        days = self.group_by_day()
        all_freqs = [[] for x in range(24)]
        for day,cmds in sorted(days.items()):
            day_times = [cmd.timestamp_struct.tm_hour for cmd in cmds]
            freq_counter = Counter(day_times)
            freqs = [0 for x in range(24)]
            for hour,num in freq_counter.items():
                freqs[hour] = num
            for hour,num in enumerate(freqs):
                all_freqs[hour].append(num)
        means = []; stdevs = []
        for hour_freqs in all_freqs:
            means.append(statistics.mean(hour_freqs))
            stdevs.append(statistics.stdev(hour_freqs))
        return means,stdevs

    def get_weekday_breakdowns(self):
        days = self.group_by_day()
        all_freqs = [[] for x in range(7)]
        for day,cmds in sorted(days.items()):
            weekdays = [cmd.timestamp_struct.tm_wday for cmd in cmds]
            freq_counter = Counter(weekdays)
            freqs = [0 for x in range(7)]
            for day,num in freq_counter.items():
                freqs[day] = num
            for day,num in enumerate(freqs):
                all_freqs[day].append(num)
        means = []; stdevs = []
        for day_freqs in all_freqs:
            means.append(statistics.mean(day_freqs))
            stdevs.append(statistics.stdev(day_freqs))
        return means,stdevs

    def get_command_lengths(self):
        lengths = [(len(cmd.base_command),cmd) for cmd in self.commands]
        sortedLengths = sorted(lengths,key=lambda x: x[0],reverse=True)
        for c_len,cmd in sortedLengths[0:5]:
            print("  {}: {}".format(c_len,cmd.base_command))
        return [len(cmd.base_command) for cmd in self.commands]

    def group_by_day(self):
        ts = [(cmd.timestamp_struct,cmd) for cmd in self.commands]
        kv = groupByKey(
            [("{}-{}-{}".format(t.tm_year,t.tm_mon,t.tm_mday),cmd)
             for t,cmd in ts])
        return kv

    def get_base_commands(self):
        return [cmd.base_command for cmd in self.commands]

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--history-dir',type=str,default="data")
    parser.add_argument('--analysis-dir',type=str,default="analysis")
    parser.add_argument('--plots-dir',type=str,default="plots")

    subparsers = parser.add_subparsers(help='sub-command help',dest='cmd')
    subparsers.required = True
    parser_timeFrequencies = subparsers.add_parser('timeFrequencies')
    parser_topCommands = subparsers.add_parser('topCommands')
    parser_topCommands.add_argument("--num",type=int,default=15)
    parser_commandLengths = subparsers.add_parser('commandLengths')

    args = parser.parse_args()

    def mkdir_p(path):
        try: os.makedirs(path)
        except: pass
    mkdir_p(args.analysis_dir)
    mkdir_p(args.plots_dir)

    hist_files = [args.history_dir+"/"+x for x in os.listdir(args.history_dir)]
    all_hist = HistoryData(hist_files)

    if args.cmd == 'timeFrequencies':
        hour_means, hour_stdevs = all_hist.get_hourly_breakdowns()
        with open(args.analysis_dir+"/time-hours.csv","w") as f:
            f.write(",".join([str(h) for h in hour_means])+"\n")
            f.write(",".join([str(h) for h in hour_stdevs])+"\n")

        wday_means, wday_stdevs = all_hist.get_weekday_breakdowns()
        with open(args.analysis_dir+"/time-wdays.csv","w") as f:
            f.write(",".join([str(h) for h in wday_means])+"\n")
            f.write(",".join([str(h) for h in wday_stdevs])+"\n")
    elif args.cmd == 'topCommands':
        cmds = all_hist.get_base_commands()
        with open(args.analysis_dir+"/top-cmds.csv","w") as f:
            print("Frequency | Command")
            print("---|---")
            f.write("{},{}\n".format("Frequency","Command"))
            for tup in Counter(cmds).most_common(args.num):
                print("{} | {}".format(tup[1],tup[0]))
                f.write("{},{}\n".format(tup[1],tup[0]))
    elif args.cmd == 'commandLengths':
        cmd_lengths = all_hist.get_command_lengths()
        with open(args.analysis_dir+"/cmd-lengths.csv","w") as f:
            f.write(",".join([str(h) for h in cmd_lengths])+"\n")
