#!/usr/bin/env python3
from collections import Counter, defaultdict
from itertools import groupby
import argparse
import os
import shutil
import statistics
import sys
import time
import warnings


try:
    from termgraph.termgraph import chart
except ImportError:
    chart = None


def groupByKey(m):
    groupedM = defaultdict(list)
    for k, v in m:
        groupedM[k].append(v)
    return groupedM


class Command:
    def __init__(self, raw):
        tup = raw.split(";")
        # TODO: Should this be hard-coded?
        self.timestamp_epoch = int(tup[0][2:-2])
        self.timestamp_struct = time.gmtime(self.timestamp_epoch)
        self.full_command = tup[1]
        self.base_command = tup[1].split()[0]


class HistoryData:
    def __init__(self, filenames):
        if isinstance(filenames, str):
            filenames = [filenames]
        commands = []
        for filename in filenames:
            with open(filename, 'rb') as f:
                it = iter(f)
                for line in it:
                    try:
                        full_line = line.decode()
                        while full_line.strip()[-1] == '\\':
                            full_line += next(it).decode()
                        commands.append(Command(full_line))
                    except Exception as e:
                        # print("Warning: Exception parsing.")i
                        # print(e)
                        pass
        self.commands = commands

    def get_hourly_breakdowns(self):
        days = self.group_by_day()
        all_freqs = [[] for x in range(24)]
        for day, cmds in sorted(days.items()):
            day_times = [cmd.timestamp_struct.tm_hour for cmd in cmds]
            freq_counter = Counter(day_times)
            freqs = [0 for x in range(24)]
            for hour, num in freq_counter.items():
                freqs[hour] = num
            for hour, num in enumerate(freqs):
                all_freqs[hour].append(num)
        return all_freqs

    def get_weekday_breakdowns(self):
        days = self.group_by_day()
        all_freqs = [[] for x in range(7)]
        for day, cmds in sorted(days.items()):
            all_freqs[cmds[0].timestamp_struct.tm_wday].append(len(cmds))
        return all_freqs

    def get_command_lengths(self):
        lengths = [(len(cmd.base_command), cmd) for cmd in self.commands]
        sortedLengths = sorted(lengths, key=lambda x: x[0], reverse=True)
        for c_len, cmd in sortedLengths[0:5]:
            print("  {}: {}".format(c_len, cmd.base_command))
        return [len(cmd.base_command) for cmd in self.commands]

    def group_by_day(self):
        ts = [(cmd.timestamp_struct, cmd) for cmd in self.commands]
        kv = groupByKey(
            [("{}-{}-{}".format(t.tm_year, t.tm_mon, t.tm_mday), cmd)
             for t, cmd in ts])
        return kv

    def get_base_commands(self):
        return [cmd.base_command for cmd in self.commands]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--history-dir', type=str, default="data")
    parser.add_argument('--analysis-dir', type=str, default="analysis")
    parser.add_argument('--plots-dir', type=str, default="plots")
    home_dir = os.environ.get("HOME","~")
    parser.add_argument('--history-file', type=str,
                        default="%s/.zsh_history" % home_dir)

    subparsers = parser.add_subparsers(help='sub-command help', dest='cmd')
    subparsers.required = True
    parser_timeFrequencies = subparsers.add_parser('timeFrequencies')
    parser_topCommands = subparsers.add_parser('topCommands')
    parser_topCommands.add_argument("--num", type=int, default=15)
    parser_commandLengths = subparsers.add_parser('commandLengths')

    args = parser.parse_args()

    def mkdir_p(path):
        try:
            os.makedirs(path)
        except:
            pass
    mkdir_p(args.analysis_dir)
    mkdir_p(args.plots_dir)
    mkdir_p(args.history_dir)
    shutil.copyfile(args.history_file, os.path.join(args.history_dir, 'history'))

    hist_files = [args.history_dir+"/"+x for x in os.listdir(args.history_dir)]
    all_hist = HistoryData(hist_files)

    if args.cmd == 'timeFrequencies':
        hourly_freqs = all_hist.get_hourly_breakdowns()
        means = []
        stdevs = []
        for hour_freqs in hourly_freqs:
            means.append(statistics.mean(hour_freqs))
            stdevs.append(statistics.stdev(hour_freqs))
        with open(args.analysis_dir+"/time-hours-stats.csv", "w") as f:
            f.write(", ".join([str(h) for h in means])+"\n")
            f.write(", ".join([str(h) for h in stdevs])+"\n")
        with open(args.analysis_dir+"/time-hours-full.csv", "w") as f:
            for hour in map(list, zip(*hourly_freqs)):
                f.write(", ".join([str(h) for h in hour])+"\n")

        if chart:
            # draw using termgraph
            print('y: Hour of Day, x: Average Commands Executed')
            labels = list(map(str, range(24)))
            data = [[x] for x in means]
            chart_args = {
                'stacked': False, 'width': 50, 'no_labels': False, 'format': '{:<5.2f}',
                'suffix': '', "vertical": False
            }
            chart(colors=[], data=data, args=chart_args, labels=labels)
        else:
            warnings.warn('Termgraph package is not installed, no graph will be drawn')

        wdays_freqs = all_hist.get_weekday_breakdowns()
        means = []
        stdevs = []
        for day_freqs in wdays_freqs:
            means.append(statistics.mean(day_freqs))
            stdevs.append(statistics.stdev(day_freqs))
        with open(args.analysis_dir+"/time-wdays-stats.csv", "w") as f:
            f.write(", ".join([str(h) for h in means])+"\n")
            f.write(", ".join([str(h) for h in stdevs])+"\n")
        with open(args.analysis_dir+"/time-wdays-full.csv", "w") as f:
            for wday in map(list, zip(*wdays_freqs)):
                f.write(", ".join([str(h) for h in wday])+"\n")
        if chart:
            # draw using termgraph
            print('y: Week Day, x: Average Commands Executed')
            labels = ("Mon","Tues","Weds","Thurs","Fri","Sat","Sun")
            data = [[x] for x in means]
            chart_args = {
                'stacked': False, 'width': 50, 'no_labels': False, 'format': '{:<5.2f}',
                'suffix': '', "vertical": False
            }
            chart(colors=[], data=data, args=chart_args, labels=labels)
    elif args.cmd == 'topCommands':
        cmds = all_hist.get_base_commands()
        with open(args.analysis_dir+"/top-cmds.csv", "w") as f:
            print("Frequency | Command")
            print("---|---")
            f.write("{},{}\n".format("Frequency", "Command"))
            mc_cmds_counter = Counter(cmds).most_common(args.num)
            for tup in mc_cmds_counter:
                print("{} | {}".format(tup[1], tup[0]))
                f.write("{},{}\n".format(tup[1], tup[0]))
            if chart:
                # draw using termgraph
                print('y: Command, x: Frequency')
                labels = [x[0] for x in mc_cmds_counter]
                data = [[x[1]] for x in mc_cmds_counter]
                chart_args = {
                    'stacked': False, 'width': 50, 'no_labels': False, 'format': '{:<5.2f}',
                    'suffix': '', "vertical": False
                }
                chart(colors=[], data=data, args=chart_args, labels=labels)
            else:
                warnings.warn('Termgraph package is not installed, no graph will be drawn')
    elif args.cmd == 'commandLengths':
        cmd_lengths = all_hist.get_command_lengths()
        with open(args.analysis_dir+"/cmd-lengths.csv", "w") as f:
            f.write(", ".join([str(h) for h in cmd_lengths])+"\n")
