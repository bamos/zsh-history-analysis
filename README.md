# Zsh History Analysis
[zsh](http://www.zsh.org/) logs commands and timestamps to `~/.zsh_history` for
shell features such as reverse history search.
This repository is a fun project that provides shell, Python, and R
scripts to parse, analyze, visualize `.zsh_history` files.
These scripts can be extended to support Bash's `.bash_history`.

Note: This is my first time using R and I am happy for improvements.

# Getting Started
You can run this on your `.zsh_history` files by cloning this repository
with `git clone https://github.com/bamos/zsh-history-analysis.git`
and installing the following prerequisites.
Ensure you have increased the history file size so commands aren't removed.
Then, follow the steps in `Control Flow` to generate the plots.

## Prerequisites
+ `PATH` contains `python3` and `Rscript`, which can be installed from
  your package manager.
  In Arch Linux, the required packages are
  [python](https://www.archlinux.org/packages/extra/x86_64/python/)
  and [r](https://www.archlinux.org/packages/extra/i686/r/).
+ `R`: [ggplot2](http://ggplot2.org/) is installed
  from an R shell with `install.packages("ggplot2")`.

## Increasing the History File Size
Unfortunately, zsh's default history file size is limited to
10000 lines by default and will truncate the history to this
length by deduplicating entries and removing old data.

Adding the following lines to `.zshrc` will remove the limits and
deduplication of the history file.

```Bash
export HISTSIZE=1000000000
export SAVEHIST=$HISTSIZE
setopt EXTENDED_HISTORY
```

## Control Flow
The following is the control flow for generating plots.

1. Archive all `.zsh_history` files in `data/<server>.zsh_history`.
`./pull-history-data.sh` is a script to partially help archiving the data
that will pull files from a list of servers separated by newlines in a
file named `servers`.
2. Run `./analyze.py` to analyze the raw data files.
`./analyze.py --help` will provide a help menu with the supported options.
3. Run `./plot.r` to generate plots from the analyzed data.

# Contributing
I'm happy to review pull requests and look through issues.
The most outstanding issue preventing a lot more analysis to
be added is [#1](https://github.com/bamos/zsh-history-analysis/issues/1),
which I would appreciate some ideas on.

# Sample Results
Following is a snapshot of results from my computers over
the last few months.

## Command Frequencies
At a given hour or weekday, how frequently do I run commands?
The following shows the average number of commands executed
for each hour and weekday.
I average 10 commands per hour overnight and
a little more during the day, and Wednesdays seem to be
my least productive days.

![](https://github.com/bamos/zsh-history-analysis/raw/master/sample-results/time-hours-bar.png)
![](https://github.com/bamos/zsh-history-analysis/raw/master/sample-results/time-wdays-bar.png)

Many hours have 0 commands executed since I'm not typing commands every hour of
every day, so these points have a high standard deviation.
[Empirical Cumulative Distribution Functions (ECDF's)](http://en.wikipedia.org/wiki/Empirical_distribution_function)
provide a deeper visualization of the distributions.

![](https://github.com/bamos/zsh-history-analysis/raw/master/sample-results/time-hours-ecdf.png)
![](https://github.com/bamos/zsh-history-analysis/raw/master/sample-results/time-wdays-ecdf.png)

## Average command length
[.aliases](https://github.com/bamos/dotfiles/blob/master/.aliases) in my
[dotfiles repo](https://github.com/bamos/dotfiles)
is a list of short aliases mostly one to two characters in length.
This plot shows the ECDF of the base commands and aliases.

![](https://github.com/bamos/zsh-history-analysis/raw/master/sample-results/cmd-lengths-full.png)

What command was over 100 characters!?
`analyze.py` will output the top five commands, and these
long commands are from using the full path to an executable,
such as the Android ARM cross compiler, as shown in the following output.

```Bash
$ ./analyze.py commandLengths
  105: /opt/android-ndk-r9/toolchains/arm-linux-androideabi-4.8/prebuilt/linux-x86/bin/arm-linux-androideabi-gcc
```

Scoping into the majority of the data shows that almost 50% of my
commands are one or two characters.

![](https://github.com/bamos/zsh-history-analysis/raw/master/sample-results/cmd-lengths-zoomed.png)

## Top Commands
Since almost 50% of my commands are one or two characters,
what are the top commands?
The following plot shows the top commands are Linux utilities
and [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) aliases.

![](https://github.com/bamos/zsh-history-analysis/raw/master/sample-results/top-cmds.png)

# Similar Projects
+ [This post](http://www.smallmeans.com/notes/shell-history/)
gives a one-liner to produces a text-based histogram of the top commands.
