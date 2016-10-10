#!/bin/sh
cd test/
failed=0
run=0
for file in *.test
do
    echo "Running $file"
    let "run += 1"
    if ! python test.py $file
    then
        let "failed += 1"
    fi
done
echo "Run $run, failed $failed"
if ((failed > 0))
then
    exit 1
fi
