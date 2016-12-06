#!/bin/sh

PIP=pip
PIP=pip3
NAME=mount
sudo -H $PIP install --quiet --upgrade ${NAME}
$PIP show ${NAME} | grep -e "^Version"
