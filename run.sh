#!/bin/bash

echo "============================================"
echo " Student Behaviour Analysis - Run Pipeline"
echo "============================================"

# ============================================
# Step 1: Activate virtual environment
# ============================================

if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found. Run setup.sh first."
    exit 1
fi

# ============================================
# Step 2: Check required folders
# ============================================

echo "Checking project structure..."
mkdir -p models/trained_models
mkdir -p outputs/csv

# ============================================
# Step 3: Run YOLO
# ============================================

echo ""
echo "Step 1: Running YOLO training..."
python -m custom_yolo.main
if [ $? -ne 0 ]; then
    echo "YOLO step failed"
    exit 1
fi

# ============================================
# Step 4: Run CV Pipeline
# ============================================

echo ""
echo "Step 2: Running Computer Vision pipeline..."
python -m cv_pipelines.main
if [ $? -ne 0 ]; then
    echo "CV pipeline failed"
    exit 1
fi

# ============================================
# Step 5: Run ML Training
# ============================================

echo ""
echo "Step 3: Running ML training..."
python -m ml.main
if [ $? -ne 0 ]; then
    echo "ML training failed"
    exit 1
fi

# ============================================
# Step 6: Run Full Main Pipeline
# ============================================

echo ""
echo "Step 4: Running full pipeline..."
python -m main
if [ $? -ne 0 ]; then
    echo "Main pipeline failed"
    exit 1
fi

# ============================================
# Step 7: Done
# ============================================

echo ""
echo "============================================"
echo " 🎉 Pipeline executed successfully!"
echo "============================================"

echo ""
echo "Outputs:"
echo "- YOLO model: runs/trained_models/weights/best.pt"
echo "- CSV output: outputs/csv/student_summary.csv"
echo "- ML models: models/trained_models/"
