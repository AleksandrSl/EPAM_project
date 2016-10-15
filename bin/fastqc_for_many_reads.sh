#!/bin/bash
for f in $@
do
  echo "Processing $f file..."
    fastqc $f
done

