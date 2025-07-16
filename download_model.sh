#!/bin/bash
set -e
mkdir -p Final_predictive_model
curl -L -o Final_predictive_model/finalized_model.sav "https://drive.google.com/uc?export=download&id=1y60p2JTTS2HGW98JrTo5Zi3MagUFXoEU"
echo "Model downloaded successfully." 