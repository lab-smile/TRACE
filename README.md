# 🧬 TRACE

**TRACE: Applying AI Language Models to Extract Ancestry Information from Curated Biomedical Literature**

> Automating ancestry identification in biomedical studies using GPT-4, regular expressions, and Cellosaurus crawling.

---

## Description

**TRACE (Tool for Researching Ancestry and Cell Extraction)** is a Python-based, open-source research tool that automates the extraction of ancestry-related information from biomedical research articles. TRACE identifies human cell lines or primary cultures mentioned in scientific texts and determines their associated ancestry by tracing external metadata (e.g., via Cellosaurus).

It uses a hybrid approach combining:

* **Regex-based extraction**
* **GPT-4-powered language understanding**
* **Web crawling to Cellosaurus**

TRACE was developed to address equity and transparency gaps in biomedical research, specifically the frequent underreporting and overrepresentation of certain ancestries in cell-based studies.

---

## Abstract

Ancestry reporting is essential to ensure transparency and proper representation in biomedical studies. However, manually extracting this information from study texts is time-consuming and inefficient. In this paper, we present **TRACE**, powered by GPT-4 and web crawling, to automate ancestry identification by detecting cell lines or cultures in texts and tracing their ancestry. We validated TRACE against a manually curated dataset and found substantial overrepresentation of European/White samples and widespread underreporting. TRACE enables large-scale, systematic ancestry analysis—a valuable resource for researchers and policymakers aiming to evaluate and improve representation in biomedical research.

---

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Command-Line Arguments](#command-line-arguments)
* [Examples](#examples--demos)
* [Configuration](#configuration)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors--affiliations)
* [Citation](#citation)
* [FAQ](#faq)

---

## Installation

```bash
git clone https://github.com/lab-smile/TRACE.git
cd TRACE
pip install pandas PyPDF2 openai argparse matplotlib seaborn fuzzywuzzy
```

Set your OpenAI API key:

```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

---

## Usage

### Batch Mode

```bash
python main.py \
  --batch \
  --directory path/to/papers \
  --output path/to/results \
  --score 50.0 \
  --progress \
  --curate \
  --post-process \
  --run_name "run_001"
```

### Single File

```bash
python main.py \
  --file paper.pdf \
  --output results/
```

---

## Command-Line Arguments

| Argument                | Description                                                |
| ----------------------- | ---------------------------------------------------------- |
| `-b`, `--batch`         | Run in batch mode on a folder of PDFs                      |
| `-d`, `--directory`     | Input directory for PDFs (batch mode)                      |
| `-f`, `--file`          | Path to a single PDF file                                  |
| `-o`, `--output`        | **\[Required]** Output directory                           |
| `-v`, `--verbose`       | Print detailed logs                                        |
| `-p`, `--progress`      | Display progress bar                                       |
| `-ts`, `--test`         | Enable test mode (included for model evaluation purposes)  |
| `-tr`, `--truth`        | Path to ground truth CSV (included just for testing)       |
| `-s`, `--score`         | Similarity threshold for match filtering (default: 50.0)   |
| `-c`, `--curate`        | Filter similar cultures to select optimal match            |
| `-pp`, `--post-process` | Remove cell lines not found in original text               |
| `-r`, `--run_name`      | Optional name for batch run folder                         |

---

## Examples / Demos

* Run `test.sh` or `test.py` to evaluate model accuracy.
* Try `webCrawler/` modules to enrich cell line metadata.
* Analyze results with `matplotlib` and `seaborn` in the `notebooks/` folder (optional).

---

## Configuration

* Requires GPT access via OpenAI API key.
* Input is one or more PDF files.
* Output is a CSV with cell line names, mentions, inferred ancestry.

---

## Project Structure

```
TRACE/
├── chatgpt/              # GPT-based prompts and LLM logic
├── regularExpression/    # Regex matchers
├── testhelper/           # Accuracy validation helpers
├── utils/                # Helper functions
├── webCrawler/           # Cellosaurus enrichment
├── main.py               # Core entry point
├── test.py / test.sh     # Evaluation tools
├── LICENSE
├── README.md
```

---

## 🤝 Contributing

We welcome pull requests, feedback, and feature suggestions.
Please see `CONTRIBUTING.md` (coming soon) for contribution guidelines.

---

## License

MIT License. See [LICENSE](./LICENSE)

---

## Authors & Affiliations

* **Alison M. Veintimilla¹** – ORCID: [0009-0003-4648-7539](https://orcid.org/0009-0003-4648-7539)
* **Chintan K. Acharya²** – ORCID: [0009-0000-8761-9137](https://orcid.org/0009-0000-8761-9137)
* **Connie J. Mulligan³** – ORCID: [0000-0002-4360-2402](https://orcid.org/0000-0002-4360-2402)
* ***Ruogu Fang²,⁴\**** – ORCID: [0000-0003-3980-3532](https://orcid.org/0000-0003-3980-3532)
* ***Erika Moore¹\**** – ORCID: [0000-0003-2192-6147](https://orcid.org/0000-0003-2192-6147)

**Affiliations:**

1. University of Maryland, Fischell Department of Bioengineering
2. University of Florida, Department of Computer and Information Science
3. University of Florida, Department of Anthropology, Genetics Institute
4. University of Florida, J. Crayton Pruitt Family Department of Biomedical Engineering

**Contact:**

* 📧 Erika Moore: [emt@umd.edu](mailto:emt@umd.edu)
* 📧 Ruogu Fang: [ruogu.fang@ufl.edu](mailto:ruogu.fang@ufl.edu)

---

## Citation

If you use TRACE in your work, please cite it as:

```bibtex
@misc{veintimilla2025trace,
  title     = {TRACE: Applying AI Language Models to Extract Ancestry Information from Curated Biomedical Literature},
  author    = {Veintimilla, Alison M. and Acharya, Chintan K. and Mulligan, Connie J. and Fang, Ruogu and Moore, Erika},
  year      = {2025},
  howpublished = {\url{https://github.com/yourusername/TRACE}}
}
```

---

## Keywords

* Ancestry Representation
* Automated Text Mining
* Cell Line Identification
* Biomedical Research Equity
* Cell Cultures
* Large Language Models (LLMs)

---

## FAQ

**Q: Does TRACE work on non-human cells?**
A: No, TRACE is optimized for human cell line detection and ancestry estimation.

**Q: Can I use it without OpenAI/GPT?**
A: Yes, regex-only mode will partially work, but GPT enhances accuracy. We are also working on providing 

**Q: How is ancestry determined?**
A: TRACE matches the detected cell line to Cellosaurus entries and parses ancestry metadata using GPT.
