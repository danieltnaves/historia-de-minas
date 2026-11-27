#!/bin/zsh
# print plain text of fragments given as numbers
for n in "$@"; do f=text/p$(printf %03d $n).html; echo "=== $f"; sed -E 's/<!-- p\. ([0-9]+) -->/\n[[p.\1]]/g; s/<figure[^>]*>.*<\/figure>/[FIG]/; s/<[^>]+>//g' $f; done
