#!/bin/bash

echo "[bash runner] Now running SAMPLe..."
echo "[bash runner] using SAMPLe_algorithm/Python3/unit/main.py"
echo "[bash runner] check at SAMPLe_algorithm/Python3/.data.toml"
echo "[bash runner] Now running..."
python3 /SAMPLe_algorithm/Python3/unit/main.py || bash onRunError.sh
