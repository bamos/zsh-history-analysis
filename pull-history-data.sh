#!/bin/bash

mkdir -p data

set -x
while read SERVER; do
  rsync $SERVER:~/.zsh_history data/$SERVER-zsh_history
done<servers
