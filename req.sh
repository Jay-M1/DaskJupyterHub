#!/usr/bin/env bash
for dir in rocky coffea-backup jupy/notebook; do
    cp requirements.txt $dir/requirements.txt
done
