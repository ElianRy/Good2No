#!/bin/bash
cd /home/claude/g2n/lot7/$1 && rm -rf *_parts && python3 video.py > render.log 2>&1 && echo "$1 OK $(date +%H:%M)" >> ../render_status2.txt || echo "$1 FAIL" >> ../render_status2.txt
