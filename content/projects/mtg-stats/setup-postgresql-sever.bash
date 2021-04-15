#!/bin/bash
packagelist=(
    postgresql
    python
    git
) 

apt-get install ${packagelist[@]}
