#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=12GB
#SBATCH --partition=hpg-ai
#SBATCH --gpus=a100:1
#SBATCH --time=12:00:00
#SBATCH --output=output/NewResults/%x.%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@example.com

pwd
date
module load singularity

# Define common variables
SINGULARITY_IMAGE="/path/to/your/singularity/image"
INPUT_DIRECTORY="/path/to/your/input/directory"
OUTPUT_DIRECTORY="/path/to/your/output/directory"
TRUTH_FILE="/path/to/your/truth/file.csv"
SCORE_VALUE=50.0

# Run 1 (with post-process)
singularity exec --bind /red --nv $SINGULARITY_IMAGE python /path/to/your/main.py \
    --task ChatGPT \
    --batch \
    --directory $INPUT_DIRECTORY \
    --test-similarity \
    --truth-file $TRUTH_FILE \
    --score $SCORE_VALUE \
    --output-directory $OUTPUT_DIRECTORY \
    --post-process \
    --run "batch_run_1"

# Run 2 (without post-process)
singularity exec --bind /red --nv $SINGULARITY_IMAGE python /path/to/your/main.py \
    --task ChatGPT \
    --batch \
    --directory $INPUT_DIRECTORY \
    --test-similarity \
    --truth-file $TRUTH_FILE \
    --score $SCORE_VALUE \
    --output-directory $OUTPUT_DIRECTORY \
    --run "batch_run_1"
