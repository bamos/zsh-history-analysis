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
p <- ggplot() +
  stat_ecdf(aes(x=hours[[1]])) +
  stat_ecdf(aes(x=hours[[2]])) +
  stat_ecdf(aes(x=hours[[3]])) +
  stat_ecdf(aes(x=hours[[4]])) +
  stat_ecdf(aes(x=hours[[5]])) +
  stat_ecdf(aes(x=hours[[6]])) +
  stat_ecdf(aes(x=hours[[7]])) +
  stat_ecdf(aes(x=hours[[8]])) +
  stat_ecdf(aes(x=hours[[9]])) +
  stat_ecdf(aes(x=hours[[10]])) +
  stat_ecdf(aes(x=hours[[11]])) +
  stat_ecdf(aes(x=hours[[12]])) +
  stat_ecdf(aes(x=hours[[13]])) +
  stat_ecdf(aes(x=hours[[14]])) +
  stat_ecdf(aes(x=hours[[15]])) +
  stat_ecdf(aes(x=hours[[16]])) +
  stat_ecdf(aes(x=hours[[17]])) +
  stat_ecdf(aes(x=hours[[18]])) +
  stat_ecdf(aes(x=hours[[19]])) +
  stat_ecdf(aes(x=hours[[20]])) +
  stat_ecdf(aes(x=hours[[21]])) +
  stat_ecdf(aes(x=hours[[22]])) +
  stat_ecdf(aes(x=hours[[23]])) +
  stat_ecdf(aes(x=hours[[24]])) +
  theme(legend.title=element_blank()) +
  xlab("Number of Hourly Commands") +
  ylab("") +
  theme_bw()
ggsave("plots/time-hours-ecdf.png",width=7,height=6)

wdays_m = as.numeric(read.csv("analysis/time-wdays-stats.csv",header=F,nrows=1))
wdays_stdev = as.numeric(read.csv("analysis/time-wdays.csv",header=F,nrows=1,skip=1))
wday_str = c("Mon","Tues","Weds","Thurs","Fri","Sat","Sun")
df <- data.frame(freqs = wdays_m, wdays = factor(wday_str,levels=wday_str),
                 stdev=wdays_stdev)
limits <- aes(ymax = freqs + stdev, ymin=freqs - stdev)
p <- ggplot(df,aes(x=wdays,y=freqs)) +
  xlab("Week Day") +
  ylab("Average Commands Executed") +
  geom_bar(stat='identity',aes(y=freqs)) +
  #geom_errorbar(limits, width=0.25) +
  theme_bw()
ggsave("plots/time-wdays-bar.png",width=7,height=6)

wdays = read.csv("analysis/time-wdays-full.csv",header=F)
p <- ggplot() +
  stat_ecdf(data=data.frame(wdays[[1]]),aes(x=wdays[[1]],colour="m")) +
  stat_ecdf(data=data.frame(wdays[[2]]),aes(x=wdays[[2]],colour="t")) +
  stat_ecdf(data=data.frame(wdays[[3]]),aes(x=wdays[[3]],colour="w")) +
  stat_ecdf(data=data.frame(wdays[[4]]),aes(x=wdays[[4]],colour="th")) +
  stat_ecdf(data=data.frame(wdays[[5]]),aes(x=wdays[[5]],colour="f")) +
  stat_ecdf(data=data.frame(wdays[[6]]),aes(x=wdays[[6]],colour="s")) +
  stat_ecdf(data=data.frame(wdays[[7]]),aes(x=wdays[[7]],colour="su")) +
  scale_color_manual(
      name="",
      breaks = c("m","t","w","th","f","s","su"),
      values = c("m"="#CCE5FF", "t"="#99CCFF", "w"="#66B2FF", "th"="#3399FF",
                 "f"="#0080FF", "s"="#0066CC", "su"="#004C99"),
      labels = c("m"="Mon", "t"="Tues", "w"="Weds", "th"="Thurs", "f"="Fri",
                 "s"="Sat", "su"="Sun")
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
