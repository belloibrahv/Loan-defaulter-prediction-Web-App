#!/bin/bash
set -e

echo "Downloading model file..."
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1ilheUO6yfL7u3ibsaEcI5ZpBGETYLqrR' -O Final_predictive_model/finalized_model.sav

# Optional: Check if the file is HTML (which means the download failed)
if file Final_predictive_model/finalized_model.sav | grep -q 'HTML'; then
  echo "Downloaded file is HTML, not a model! Check your Google Drive link or permissions."
  exit 1
fi

echo "Model downloaded successfully." 