#!/usr/bin/env Rscript

# library(extrafont) # First time: Run font_import() in R shell.
# loadfonts()

library(ggplot2)
library(reshape)

hours = as.numeric(read.csv("analysis/time-hours.csv",header=F))

p <- ggplot() +
  xlab("Hour of Day") +
  ylab("Total Commands Executed") +
  geom_histogram(aes(x=hours),binwidth=1) +
  theme_bw()
ggsave("plots/time-hours.pdf",width=7,height=6)


wdays = as.numeric(read.csv("analysis/time-wdays.csv",header=F))
p <- ggplot() +
  xlab("Week Day") +
  ylab("Total Commands Executed") +
  geom_histogram(aes(x=wdays),binwidth=1) +
  theme_bw()
ggsave("plots/time-wdays.pdf",width=7,height=6)