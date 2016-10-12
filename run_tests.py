#!/bin/python3
from test.test import run_test
from sys import exit
import os
failed = 0
run = 0
os.chdir("test/")
for test_file in os.listdir(path='.'):
    if test_file.endswith(".test"):
        print("Running $file")
        run += 1
        if not run_test(test_file):
            failed += 1
print("Run {}, failed {}".format(run, failed))
if failed > 0:
    exit(1)
