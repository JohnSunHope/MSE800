# test_conda_python

Small utility to verify `conda` availability and run a couple of simple Python function tests.

Run:

```bash
python3 test_conda_python.py
```

Exit codes:
- `0`: conda detected and functions passed
- `1`: conda not detected but functions passed
- `2`: function tests failed
