#!/bin/bash

echo "============================================"
echo " Student Behaviour Analysis - Setup"
echo "============================================"

# ============================================
# Step 1: Check Python
# ============================================

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found. Please install Python 3.9+ and try again."
    exit 1
fi

python3 --version

# ============================================
# Step 2: Create Virtual Environment
# ============================================

echo "Creating virtual environment..."
python3 -m venv venv

# ============================================
# Step 3: Activate Virtual Environment
# ============================================

echo "Activating virtual environment..."
source venv/bin/activate

# ============================================
# Step 4: Upgrade pip
# ============================================

echo "Upgrading pip..."
pip install --upgrade pip

# ============================================
# Step 5: Install dependencies
# ============================================

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Installing basic dependencies..."
    pip install numpy pandas scikit-learn opencv-python ultralytics torch transformers peft datasets
fi

# ============================================
# Step 6: Create required folders
# ============================================

echo "Creating project folders..."
mkdir -p models/trained_models
mkdir -p outputs/csv

# ============================================
# Step 7: Environment variables
# ============================================

echo ""
echo "If using LLM (Gemini), set your API key like:"
echo "export GEMINI_API_KEY='your_api_key_here'"
echo "export GEMINI_MODEL='gemini-2.0-flash'"
echo ""

# ============================================
# Step 8: Verify installation
# ============================================

echo "Verifying installation..."
python - <<END
import numpy, pandas, sklearn, cv2, torch
print("All core packages installed successfully")
END

echo ""
echo "============================================"
echo " Setup Completed Successfully!"
echo "============================================"

echo "To activate environment later:"
echo "source venv/bin/activate"

echo "To run project:"
echo "python -m main"