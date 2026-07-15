#!/bin/bash

echo "========================================="
echo " 1. AVVIO SOLUTORE (simpleFoam)"
echo "========================================="
# Esegue simpleFoam pulito
simpleFoam

if [ $? -ne 0 ]; then
    echo "[ERRORE DI SISTEMA] simpleFoam si è interrotto."
    exit 1
fi

echo "========================================="
echo " 2. ELABORAZIONE GRAFICI (Python)"
echo "========================================="
# Lancia il post-processing Python
python3 auto_postprocess.py

touch case.foam