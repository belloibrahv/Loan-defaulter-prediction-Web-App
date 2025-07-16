#!/bin/bash
set -e
mkdir -p Final_predictive_model
curl -L -o Final_predictive_model/finalized_model.sav "https://drive.google.com/file/d/1y60p2JTTS2HGW98JrTo5Zi3MagUFXoEU/view?usp=sharing"
echo "Model downloaded successfully." 