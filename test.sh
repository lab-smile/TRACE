#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=12GB
#SBATCH --partition=hpg-ai
#SBATCH --gpus=a100:1
#SBATCH --time=12:00:00
#SBATCH --output=output/%x.%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=dev@thecka.tech

pwd
date
module load singularity

# Define common variables
SINGULARITY_IMAGE="/blue/ruogu.fang/chintan.acharya/monaicore1.3.0"
INPUT_FILE="/blue/ruogu.fang/chintan.acharya/smile-lab/Ancestry/RegexAndChatgpt/papers/Science_of_Translational_Medicine/sample.pdf"
OUTPUT_DIR="/blue/ruogu.fang/chintan.acharya/smile-lab/Ancestry/NewResults"
TRUTH_FILE="/blue/ruogu.fang/chintan.acharya/smile-lab/Ancestry/RegexAndChatgpt/truth/cultures_1.csv"
PREFIX="9_filtered"
SCORE=50.0

# Command for single file testing
CMD="singularity exec --bind /red --nv $SINGULARITY_IMAGE python test.py -t ChatGPT -f \"$INPUT_FILE\" -v -p --test --truth \"$TRUTH_FILE\" -s $SCORE --prefix \"$PREFIX\" -o \"$OUTPUT_DIR\""

# Run the command
$CMD
