#!/bin/bash

mkdir -p data

while read SERVER; do
  rsync $SERVER:~/.zsh_history data/$SERVER-zsh_history
done<servers
