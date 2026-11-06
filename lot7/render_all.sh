#!/bin/bash
cd /home/claude/g2n/lot7
for k in chaise viande fleming; do
  (cd $k && rm -rf *_parts && python3 video.py > render.log 2>&1 && echo "$k OK $(date +%H:%M)" >> ../render_status.txt || echo "$k FAIL" >> ../render_status.txt)
done
