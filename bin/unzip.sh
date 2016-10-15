#!/bin/bash 
for f in $@
do
  echo "Processing $f file..."
    gunzip $f
done
