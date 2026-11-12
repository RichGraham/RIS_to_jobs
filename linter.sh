#!/usr/bin/env bash
echo '!!!!! Consider also running: codeFeedback.sh in src directory !!!!!'
echo '==== src ===='
ruff check --fix src/*.py --select C
ruff check --fix src/*.py
echo '==== tests ===='
ruff check --fix tests/*.py --select C
