#!/usr/bin/env Rscript

library(ggplot2)
library(reshape)

hours_m = as.numeric(read.csv("analysis/time-hours-stats.csv",header=F,nrows=1))
hours_stdev = as.numeric(read.csv("analysis/time-hours-stats.csv",
                                  header=F,nrows=1,skip=1))

df <- data.frame(freqs=hours_m,stdev=hours_stdev)
limits <- aes(ymax = freqs + stdev, ymin=freqs - stdev)
p <- ggplot(df,aes(x=0:23,y=freqs)) +
  xlab("Hour of Day") +
  ylab("Average Commands Executed") +
  geom_bar(stat='identity') +
  #geom_errorbar(limits, width=0.25) +
  theme_bw()
ggsave("plots/time-hours-bar.png",width=7,height=6)

hours = read.csv("analysis/time-hours-full.csv",header=F)
df = melt(hours)
p <- ggplot(df, aes(x=value)) +
  stat_ecdf(aes(group = variable)) +
  theme(legend.title=element_blank()) +
  xlab("Number of Hourly Commands") +
  ylab("") +
  theme_bw()
ggsave("plots/time-hours-ecdf.png",width=7,height=6)

wdays_m = as.numeric(read.csv("analysis/time-wdays-stats.csv",header=F,nrows=1))
wdays_stdev = as.numeric(read.csv("analysis/time-wdays-stats.csv",
                                  header=F,nrows=1,skip=1))
wday_str = c("Mon","Tues","Weds","Thurs","Fri","Sat","Sun")
df <- data.frame(freqs = wdays_m, wdays = factor(wday_str,levels=wday_str),
                 stdev=wdays_stdev)
limits <- aes(ymax = freqs + stdev, ymin=freqs - stdev)
p <- ggplot(df,aes(x=wdays,y=freqs)) +
  xlab("Week Day") +
  ylab("Average Commands Executed") +
  geom_bar(stat='identity',aes(y=freqs)) +
  geom_errorbar(limits, width=0.25) +
  theme_bw()
ggsave("plots/time-wdays-bar.png",width=7,height=6)

wdays = read.csv("analysis/time-wdays-full.csv",header=F)
df <- melt(wdays)
p <- ggplot(df, aes(x=value)) +
  stat_ecdf(aes(group=variable,colour=variable)) +
  scale_color_manual(
      name="",
      values = c("#CCE5FF", "#99CCFF", "#66B2FF", "#3399FF",
                 "#0080FF", "#0066CC", "#004C99"),
      labels = c("Mon", "Tues", "Weds", "Thurs", "Fri", "Sat", "Sun")
  ) +
  theme(legend.title=element_blank()) +
  xlab("Number of Daily Commands") +
  ylab("") +
  theme_bw()
ggsave("plots/time-wdays-ecdf.png",width=7,height=6)

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

cmd_lengths = as.numeric(read.csv("analysis/cmd-lengths.csv",header=F))
df = data.frame(cmd_lengths)
p <- ggplot() +
  stat_ecdf(data=df,aes(x=cmd_lengths)) +
  xlab("Base Command Length") +
  ylab("") +
  scale_x_continuous(
      limits=c(0,max(df)),
      breaks=seq(0,max(df),10),
      minor_breaks=seq(0,max(df),5)
  ) +
  theme_bw()
ggsave("plots/cmd-lengths-full.png",width=7,height=6)

p <- ggplot() +
  stat_ecdf(data=df,aes(x=cmd_lengths)) +
  xlab("Base Command Length") +
  ylab("") +
  scale_x_continuous(
      limits=c(0,max(df)/3),
      breaks=seq(0,max(df)/3,10),
      minor_breaks=seq(0,max(df)/3,5)
  ) +
  theme_bw()
ggsave("plots/cmd-lengths-zoomed.png",width=7,height=6)
