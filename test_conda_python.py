#!/usr/bin/env python3
"""
Simple script to test whether `conda` is available and to run a few
Python function checks.

Usage: python3 test_conda_python.py
"""
import subprocess
import sys
import os
import numpy as np


def check_conda():
    try:
        res = subprocess.run(["conda", "--version"], capture_output=True, text=True, check=True)
        version = res.stdout.strip() or res.stderr.strip()
        print("conda: detected ->", version)
        in_conda_env = bool(os.environ.get("CONDA_PREFIX"))
        print("CONDA_PREFIX present:" , in_conda_env)
        return True
    except FileNotFoundError:
        print("conda: not found (FileNotFoundError)")
        return False
    except subprocess.CalledProcessError as e:
        print("conda: command failed ->", e)
        return False


def check_python():
    print("python executable:", sys.executable)
    print("python version:", sys.version.replace('\n', ' '))
    # detect if running inside a conda env
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        print("Running inside conda env at:", conda_prefix)
    else:
        print("No CONDA_PREFIX found; not necessarily a conda env")


def add(a, b):
    return a + b


def factorial(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def run_tests():
    # Basic function tests
    assert add(2, 3) == 5, "add(2,3) must be 5"
    assert add(-1, 1) == 0, "add(-1,1) must be 0"
    assert factorial(0) == 1, "factorial(0) must be 1"
    assert factorial(5) == 120, "factorial(5) must be 120"
    print("function tests: OK")


def main():
    print("--- Environment checks ---")
    conda_ok = check_conda()
    print()
    check_python()
    print()
    print("--- Running small unit tests ---")
    try:
        run_tests()
    except AssertionError as e:
        print("Tests failed:", e)
        sys.exit(2)

    print()
    if conda_ok:
        print("Overall: OK (conda available and functions passed)")
        sys.exit(0)
    else:
        print("Overall: Functions passed but conda not detected")
        sys.exit(1)


if __name__ == '__main__':
    main()
