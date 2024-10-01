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

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install pandas PyPDF2 openai argparse matplotlib seaborn
   ```
3. Set up your OpenAI API key as an environment variable

## Usage

### Running main.py

```
python /path/to/your/main.py \
    --batch \
    --directory $INPUT_DIRECTORY \
    --test-similarity \
    --progress \
    --truth-file $TRUTH_FILE \
    --score $SCORE_VALUE \
    --output-directory $OUTPUT_DIRECTORY \
    --post-process \
    --run "batch_run_1"
```
