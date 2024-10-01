import argparse
import os
import time
from collections import defaultdict
import pandas as pd
from difflib import SequenceMatcher
import re
from PyPDF2 import PdfReader

# Import custom modules
from utils.papertochunks import chunkify, extract_text_from_pdf
from utils.progressindicator import progress_bar
from utils.distribution import distribution
from regularExpression.regularExpression import findSurroundingSentences
from chatgpt.chatgpt import gptUseCultures, gptFilterList, gptForPrimaryCellCultures, filterHyphenResult
from webCrawler.webCrawler import crawlCul, crawlEth
from test import compare_csv, visualize

# Set up command-line argument parser
parser = argparse.ArgumentParser(description="Process PDF files for cell culture analysis")
parser.add_argument("-b", "--batchMode", action='store_true', help="Run on a batch of papers")
parser.add_argument("-d", "--directory", default='', type=str, help="Base directory for batch mode")
parser.add_argument("-f", "--file", default="", type=str, help="File path for individual mode")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
parser.add_argument("-p", "--progress", action="store_true", help="Show progress indication")
parser.add_argument("-ts", "--test", action="store_true", help="Run in test mode")
parser.add_argument("-tr","--truth", default="truth/cultures_1.csv", type=str, help="Path to ground truth CSV file")
parser.add_argument("-s", "--score", default=50.0, type=float, help="Similarity score threshold")
parser.add_argument("-o", "--output", default="", type=str, help="Output directory for results", required=True)
parser.add_argument("-pp", "--post-process", action="store_true", default=False, help="Apply post-processing filter")
parser.add_argument("-r", "--run_name", type=str, help="Run name for batch mode output directory", required=False)

def main():
    """Main function to orchestrate the entire process."""
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Batch mode: {'Enabled' if args.batchMode else 'Disabled'}")
    
    # Process files and get output file path
    output_file = process_batch(args) if args.batchMode else process_single_file(args)
    
    # Run tests if test mode is enabled
    if args.test:
        run_tests(args, output_file)

def process_batch(args):
    """Process a batch of PDF files."""
    if not args.run_name:
        raise ValueError("Run name is required for batch mode. Use -r or --run-name to specify.")
    
    results = []
    print(f"Processing directory: {args.directory}")
    for root, _, files in os.walk(args.directory):
        for file in sorted(files):
            if file.lower().endswith('.pdf'):
                filepath = os.path.join(root, file)
                results.append(gptRun(filepath, args.verbose, args.progress, args.post_process))
    
    # Combine results and save to CSV
    combined_results = pd.concat(results, axis=0, ignore_index=True)
    output_dir = os.path.join(args.output, args.run_name)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "res_filtered.csv" if args.post_process else "res.csv")
    combined_results.to_csv(output_file, index=False)
    print(f"Results written to {output_file}")
    
    return output_file

def process_single_file(args):
    """Process a single PDF file."""
    df = gptRun(args.file, args.verbose, args.progress, args.post_process)
    base_name = os.path.splitext(os.path.basename(args.file))[0]
    output_file = os.path.join(args.output, f"{base_name}_filtered.csv" if args.post_process else f"{base_name}.csv")
    df.to_csv(output_file, index=False)
    print(f"Results written to {output_file}")
    
    return output_file

def gptRes(filepath, verbose, progress):
    """Process file using GPT and return filtered results."""
    cultures = []
    chunk_dict = defaultdict(list)
    chunks = chunkify(filepath, verbose)

    for index, chunk in enumerate(chunks):
        chunk_cultures = gptUseCultures(chunk, verbose).split(",")
        for culture in chunk_cultures:
            culture = culture.strip()
            if culture and culture != '-':
                cultures.append(culture)
                chunk_dict[culture].append(chunk)
        
        if progress:
            progress_bar(index + 1, len(chunks), verbose=verbose)

    # Remove duplicates and filter cultures
    cultures = list(set(cultures))
    filtered_cultures = gptFilterList("cell types or cell lines or primary cell cultures or cell name", cultures, verbose).split(",")
    filtered_cultures = [culture.strip() for culture in filtered_cultures if culture.strip()]

    return filtered_cultures, chunk_dict

def webCrawl(file_id, cultures, chunk_dict, verbose, progress):
    """Perform web crawling for additional information on cultures."""
    headings = ['File Id', 'Name', 'Ancestry Available', 'Ancestry Reported', 'Found Correctly', 'Cell line name', 'Gender', 'Age', 'Category', 'Ancestry from GPT', 'Ancestry from Web']
    culture_results = []

    for count, culture in enumerate(cultures, 1):
        ancestry_gpt = find_ancestry_gpt(culture, chunk_dict, verbose)
        ancestry_web, available, line_name, gender, category, age, species = perform_web_crawl(culture, verbose)
        found_correctly = check_ancestry_correctness(ancestry_gpt, ancestry_web)

        culture_results.append([
            file_id, culture, available, bool(ancestry_gpt), found_correctly,
            line_name, gender, age, category, ancestry_gpt, ancestry_web
        ])
        
        if progress:
            progress_bar(count, len(cultures), verbose=verbose)

    return pd.DataFrame(culture_results, columns=headings)

def find_ancestry_gpt(culture, chunk_dict, verbose):
    """Find ancestry using GPT."""
    for i in range(0, len(chunk_dict[culture]), 5):
        context = "".join(chunk_dict[culture][i:i+5])
        sentences = findSurroundingSentences(context, culture, 45)
        ancestry_gpt = gptForPrimaryCellCultures(culture, "".join(sentences), verbose)
        ancestry_gpt = filterHyphenResult(ancestry_gpt)
        if ancestry_gpt:
            return ancestry_gpt
    return ""

def perform_web_crawl(culture, verbose):
    """Perform web crawling for a culture."""
    query, species, names = crawlCul(culture.strip().replace(" ", "+"), verbose)
    
    for i, name in enumerate(names[:15]):
        if culture in str(name) or str(name) in culture or similar(culture, str(name)) > 0.35:
            line_name, gender, category, age, species, table = crawlEth(query[i], verbose)
            
            if not table.empty:
                table = table.sort_values(by='% genome', ascending=False)
                ancestry_web = table.iloc[0]['Origin']
                return ancestry_web, True, line_name, gender, category, age, species
    
    return "Not Available", False, "", "", "", "", ""

def check_ancestry_correctness(ancestry_gpt, ancestry_web):
    """Check if the ancestry found by GPT is correct."""
    if ancestry_gpt and ancestry_web != "Not Available":
        ancestry_distribution = distribution.get(ancestry_web, [])
        max_similarity = max((similar(ancestry_gpt, anc) for anc in ancestry_distribution), default=0)
        return max_similarity > 0.8
    return False

def gptRun(filepath, verbose, progress, post_process=False):
    """Run GPT analysis on a file and apply postprocess filter."""
    start_time = time.time()
    if verbose:
        print(f"Starting GPT analysis on file: {filepath}")
    
    filtered_cultures, chunk_dict = gptRes(filepath, verbose, progress)
    
    if verbose:
        print(f"Found {len(filtered_cultures)} cultures")
        print("Starting web crawling for additional information")
    
    df = webCrawl(os.path.basename(filepath), filtered_cultures, chunk_dict, verbose, progress)
    df = df.drop_duplicates()
    
    # Apply postprocess filter
    df_filtered = apply_postprocess_filter(df, filepath, verbose) if post_process else df
    
    end_time = time.time()
    if verbose:
        print(f"GPT analysis and postprocessing completed for {os.path.basename(filepath)}")
        print(f"Cultures found: {len(df)} | Cultures after filtering: {len(df_filtered)}")
    print(f"Time taken for {os.path.basename(filepath)}: {end_time - start_time:.2f} seconds")
    
    return df_filtered

def apply_postprocess_filter(df, filepath, verbose):
    """Apply postprocess filter to remove cultures not found in original text."""
    if verbose:
        print("Applying postprocess filter...")
    
    text = extract_text_from_pdf(filepath, verbose)
    rows_to_keep = [index for index, row in df.iterrows() if re.search(re.escape(row['Name']), text)]
    
    if verbose:
        removed_cultures = set(df.index) - set(rows_to_keep)
        for index in removed_cultures:
            print(f"Removing culture: {df.loc[index, 'Name']} (not found in original text)")
    
    return df.loc[rows_to_keep]

def similar(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def run_tests(args, output_file):
    """Run tests and generate visualizations."""
    # Create directory structure
    input_file_name = args.run_name if args.batchMode else os.path.splitext(os.path.basename(output_file))[0]
    test_dir = os.path.join(args.output, input_file_name)
    csv_dir = os.path.join(test_dir, "csv")
    images_dir = os.path.join(test_dir, "images")
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    # Redirect print output to a file
    log_file = os.path.join(test_dir, "test_output.txt")
    with open(log_file, 'w') as f:
        import sys
        original_stdout = sys.stdout
        sys.stdout = f
        
        comparison_df, paper_wise_df = compare_csv(args.truth, output_file, args.score)
        
        # Save CSV files
        comparison_df.to_csv(os.path.join(csv_dir, "Comparison.csv"), index=False)
        paper_wise_df.to_csv(os.path.join(csv_dir, "PaperWise.csv"), index=False)
        
        # Generate visualizations
        visualize(paper_wise_df, images_dir)
        
        # Restore stdout
        sys.stdout = original_stdout
    
    print(f"Test results saved in {test_dir}")
    print(f"CSV files saved in {csv_dir}")
    print(f"Images saved in {images_dir}")
    print(f"Test output log saved to {log_file}")

if __name__ == "__main__":
    main()