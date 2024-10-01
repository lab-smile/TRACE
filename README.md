# TRACE
TRACE: Tool for Researching Ancestry and Cell Extraction

This project is designed to analyze scientific texts for mentions of human cell cultures and their associated ethnicities or races. It uses a combination of regular expression matching and AI-powered text analysis to extract relevant information from research papers.

## Features

- Supports both single file and batch processing modes
- Uses regular expressions and ChatGPT for analysis
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

For batch processing without post-processing:
```
python main.py -t ChatGPT -b -d <INPUT_DIR> -v -p --test --truth <TRUTH_FILE> -s <SIMILARITY_SCORE> --prefix <PREFIX_FOR_OUTPUT> -o <OUTPUT_DIR> -r <RUN_NAME>
```

For single file processing:
```
python main.py -t ChatGPT -f <INPUT_FILE> -v -p --test --truth <TRUTH_FILE> -s <SIMILARITY_SCORE> --prefix <PREFIX_FOR_OUTPUT> -o <OUTPUT_DIR>
```

