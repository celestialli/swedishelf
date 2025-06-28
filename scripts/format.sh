#!/bin/bash

echo "== Running: ruff format ."
ruff format .
# ruff format . --check

echo "== Running: ruff check . --select I --fix"
ruff check . --select I --fix
