#!/bin/bash
# This script runs the test suite for the cell culture analysis project

# Load required modules
module load singularity

# Define common variables
SINGULARITY_IMAGE="/path/to/your/singularity/image"
GPT_FILE="/path/to/your/input/file"
OUTPUT_DIRECTORY="/path/to/your/output/directory"
TRUTH_FILE="/path/to/your/truth/file.csv"
SCORE_VALUE=50.0

# Run the test
singularity exec --bind /red --nv "$SINGULARITY_IMAGE" python test.py \
    --gpt "$GPT_FILE" \
    --truth "$TRUTH_FILE" \
    --score "$SCORE_VALUE" \
    --output "$OUTPUT_DIRECTORY"

echo "Job completed at $(date)"