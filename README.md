# TRACE
TRACE: Tool for Researching Ancestry and Cell Extraction

This project is designed to analyze scientific texts for mentions of human cell cultures and their associated ethnicities or races. It employs a combination of regular expression matching and AI-powered text analysis, utilizing ChatGPT to extract relevant information from research papers. Additionally, the project features web crawling functionality to gather supplementary data from Cellosaurus, enhancing the analysis with more comprehensive context.

## Features

- Supports both single file and batch processing modes
- Utilizes regular expressions and ChatGPT for in-depth analysis
- Web crawling functionality to gather additional information from Cellosaurus
- Progress tracking for batch operations
- Verbose output option for detailed logging

## Requirements

- Python 3.x
- Required Python packages:
  - pandas
  - PyPDF2
  - openai
  - argparse
  - matplotlib
  - seaborn
  - fuzzywuzzy

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install pandas PyPDF2 openai argparse matplotlib seaborn fuzzywuzzy
   ```
3. Set up your OpenAI API key as an environment variable

## Usage

### Running main.py

```
python /path/to/your/main.py \
    --batch \
    --directory $INPUT_DIRECTORY \
    --test \
    --progress \
    --truth $TRUTH_FILE \
    --score $SCORE_VALUE \
    --output $OUTPUT_DIRECTORY \
    --curate \
    --post-process \
    --run "batch_run_1"
```

This section explains the command-line arguments used in the script for processing PDF files related to cell culture analysis.

- `-b` or `--batch`: Enables batch processing mode, allowing the script to process multiple PDF files in a specified directory.
- `-d` or `--directory`: Specifies the base directory where the PDF files are located when running in batch mode.
- `-f` or `--file`: Indicates the file path for processing a single PDF file in individual mode.
- `-v` or `--verbose`: Activates verbose output, providing detailed logging information during execution.
- `-p` or `--progress`: Displays progress indication during batch operations, helping users track the processing status.
- `-c` or `--curate`: Enables curation of results, filtering to obtain the most optimal cultures from similar entries.
- `-ts` or `--test`: Runs the script in test mode, allowing for validation of results against a ground truth dataset.
- `-tr` or `--truth`: Specifies the path to the ground truth CSV file used for comparison in test mode.
- `-s` or `--score`: Sets the similarity score threshold for filtering results, with a default value of 50.0.
- `-o` or `--output`: Defines the output directory where results will be saved, and is a required argument.
- `-pp` or `--post-process`: Applies a post-processing filter to the results, removing cultures not found in the original text.
- `-r` or `--run_name`: Provides a name for the run, which is used to organize output files in batch mode.

