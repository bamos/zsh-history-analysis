#!/usr/bin/env Rscript

library(ggplot2)
library(reshape)

hours_m = as.numeric(read.csv("analysis/time-hours.csv",header=F,nrows=1))
hours_stdev = as.numeric(read.csv("analysis/time-hours.csv",header=F,nrows=1,skip=1))

p <- ggplot() +
  xlab("Hour of Day") +
  ylab("Average Commands Executed") +
  geom_bar(stat='identity',aes(x=0:23.,y=hours_m)) +
  theme_bw()
  # TODO: Error bars.
ggsave("plots/time-hours.png",width=7,height=6)

wdays_m = as.numeric(read.csv("analysis/time-wdays.csv",header=F,nrows=1))
wdays_stdev = as.numeric(read.csv("analysis/time-wdays.csv",header=F,nrows=1,skip=1))
wday_str = c("Mon","Tues","Weds","Thurs","Fri","Sat","Sun")
df <- data.frame(freqs = wdays_m, wdays = factor(wday_str,levels=wday_str))
p <- ggplot(df,aes(x=wdays,y=freqs)) +
  xlab("Week Day") +
  ylab("Average Commands Executed") +
  geom_bar(stat='identity',aes(y=freqs)) +
  theme_bw()
  # TODO: Error bars.
ggsave("plots/time-wdays.png",width=7,height=6)

top_cmds = read.csv("analysis/top-cmds.csv",header=T)
df <- data.frame(
  freqs = top_cmds[[1]],
  cmd_names = factor(top_cmds[[2]],levels=top_cmds[[2]])
)
p <- ggplot(df,aes(x=cmd_names,y=freqs)) +
  xlab("Command") +
  ylab("Frequency") +
  geom_bar(stat='identity',aes(y=freqs)) +
  theme_bw()
ggsave("plots/top-cmds.png",width=7,height=6)
