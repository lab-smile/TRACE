"""
This module contains functions for comparing and visualizing the results of the cell culture analysis.
It includes functions for comparing CSV files, calculating similarity scores, and generating various visualizations.
"""

# TODO: Consider breaking this file into smaller, more focused modules
# TODO: Add type hints to function parameters and return values
# TODO: Use f-strings instead of .format() for string formatting
# TODO: Consider using a configuration file for constants and file paths

from chatgpt.chatgpt import gptMatchAncestries
from testhelper.helper import dict1, dict2, similar
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import os
import argparse

# Set up command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--true", default="", type=str, help="True or Human made file", required=True)
parser.add_argument("-g", "--gpt", default="", type=str, help="GPT and web generated file", required=True)
parser.add_argument("-c", "--curated", action="store_true", help="Are the results curated?", required=True)
parser.add_argument("-s", "--score", default=50.0, type=float, help="Similarity score threshold")
parser.add_argument("-o", "--output", default="", type=str, help="Output directory for test results", required=True)

def compare_csv(true_csv, gpto_csv, curated, sim_score_thresh = 50.0):
    print("Starting Comparison.")
    true_df = pd.read_csv(true_csv)
    gpto_df = pd.read_csv(gpto_csv)

    true_df.columns = ['Name', 'Ancestry', 'Lines with Ancestry', 'Type', 'Supplier', 'Articles', 'Primary/Line', 'Notes', 'Body Part/Tissue', 'URL', 'Flag', 'Journal', 'flag']
    true_df = true_df.drop(columns = [ 'Type', 'Supplier', 'Notes', 'Body Part/Tissue', 'URL', 'Flag', 'flag'])

    gpto_df = gpto_df.drop(columns = ['Gender', 'Age', 'Category'])
    true_df = true_df[true_df['Journal'] == 'https://www.notion.so/f3f7e3cf261449c3b4b8885d49aab57d']
    gpto_df = gpto_df.fillna('')

    # Preparing data for testing
    true_dict = defaultdict(lambda : [])
    for article in list(true_df['Articles'].unique()):
        for index, row in true_df[true_df['Articles'] == article].iterrows():
            try:
                true_dict[dict2[row['Articles']]].append((index, row['Name'], row['Ancestry'], row['Lines with Ancestry']))
            except KeyError:
                break

    gpto_dict = defaultdict(lambda : [])
    for fid in list(gpto_df['File Id'].unique()):
        if dict1[int(fid[0:-4])] != "":
            for index, row in gpto_df[gpto_df['File Id'] == fid].iterrows():
                gpto_dict[int(fid[0:-4])].append((index, row['Name'], row['Ancestry Reported'], row['Ancestry Available'], row['Ancestry from Web'],row['Ancestry from GPT'], row['Type'], row['SimilarCultures']))
    
    # Arranging Results According to Papers
    graph_len_gpt = []
    graph_len_tru = []
    papers = []
    for i in range(39):
        graph_len_gpt.append(gpto_dict[i])
        graph_len_tru.append(true_dict[i])
        if len(gpto_dict[i]) > 0 or len(true_dict[i]) > 0:
            graph_len_gpt.append(gpto_dict[i])
            graph_len_tru.append(true_dict[i])
            papers.append(i)

    # Keeping Track of Scores for each papers
    paper_wise_avg_similarity_score = []
    paper_wise_ancestry_acc = []
    paper_wise_ancestry_inc = []
    paper_wise_count_match_100 = []
    paper_wise_bad_matches = []
    paper_wise_extras = []
    total_count = []
    comparison_df = []

    for i in papers:
        paper_avg_sim_score = 0
        paper_ancestry_acc = 0
        paper_ancestry_inc = 0
        paper_count_match_100 = 0
        paper_extra = len(gpto_dict[i]) - len(true_dict[i])
        paper_bad_matches = 0

        if true_dict[i] and gpto_dict[i]:

            # Finding the most similar cell culture
            for true_row in true_dict[i]:
                max_sim_score = -1
                max_sim_row = ()

                for gpto_row in gpto_dict[i]:
                    sim_score = (similar(gpto_row[1], true_row[1]) * 100)
                    if curated:
                        for similarCulture in gpto_row[-1]:
                            sim_score = max(sim_score, similar(similarCulture, true_row[1]))
                    if max_sim_score < sim_score:
                        max_sim_score = sim_score 
                        max_sim_row = gpto_row
                
                paper_avg_sim_score += max_sim_score

                # Exact Matches
                if max_sim_score == 100.0:
                    paper_count_match_100 += 1

                # Calculating the Ancestry Accuracy
                if true_row[-2] == 'Not Reported':
                    # TODO: check is both the "Ancestry from GPT" and "Ancestry from Web" is not Reported - Completed
                    if(true_row[5] == "Not Reported" and true_row == "Not Reported"):
                        paper_ancestry_acc += 1
                    else: 
                        paper_ancestry_inc += 1
                else:
                    true_result = true_dict[-1]                    
                    gpt_result = max_sim_row[5]  # Assuming GPT results are in the last column
                    web_result = max_sim_row[4]  # Assuming Web results are in the second last column
                    
                    # Create a dictionary to map web results to true results
                    similarity_dict = {
                        "European, South": "European, White",
                        "European, North": "European, White",
                        "East Asian, North": "Asian, East Asian",
                        "East Asian, South": "Asian, East Asian",
                        "South Asian": "Asian, East Asian",
                        "Native American": "Admixed or Central/South America",
                        "African": "African, Black or African American"
                    }

                    # Check if any results are "Not Reported"
                    if gpt_result == "Not Reported" and web_result == "Not Reported":
                        paper_ancestry_inc += 1  # Both not reported, increment ancestry incorrect

                    elif web_result != "Not Reported" and gpt_result == "Not Reported":
                        # Web results are reported, check against true results
                        if similarity_dict[web_result].lower() in true_result.lower():
                            paper_ancestry_acc += 1
                        else:
                            paper_ancestry_inc += 1

                    elif web_result == "Not Reported" and gpt_result != "Not Reported":
                        # Use GPT function to check ancestry
                        result = gptMatchAncestries(gpt_result, true_result)  # Assuming max_sim_row[1] is the culture name and max_sim_row[0] is the context
                        if result.lower() == "true":
                            paper_ancestry_acc += 1
                        else:
                            paper_ancestry_inc += 1


                
                # Storing the most similar row (taking the threshold into account)
                if max_sim_score >= sim_score_thresh:
                    comparison_df.append([str(i) + '.pdf', 
                                          dict1[i], 
                                          true_row[1], 
                                          max_sim_row[1], 
                                          round(max_sim_score, 2), 
                                          true_row[-1], 
                                          max_sim_row[-1]
                                         ])
                else:
                    paper_bad_matches += 1
                    comparison_df.append([str(i) + '.pdf',
                                          dict1[i], 
                                          true_row[1], 
                                          "No good match Found", 
                                          0, 
                                          true_row[-1], 
                                          "N/A"
                                         ])

        # Calculating scores 
        paper_wise_avg_similarity_score.append(paper_avg_sim_score / len(true_dict[i]))
        paper_wise_ancestry_acc.append(paper_ancestry_acc)
        paper_wise_ancestry_inc.append(paper_ancestry_inc)
        paper_wise_count_match_100.append(paper_count_match_100)
        paper_wise_extras.append(paper_extra)
        paper_wise_bad_matches(paper_bad_matches)
        total_count.append(len(true_dict[i]))

    # Creating a "Paper Wise" Dataframe
    paper_wise_df = []
    for i in range(len(papers)):
        paper_wise_df.append([str(papers[i]) + '.pdf',
                              dict1[papers[i]],
                              paper_wise_avg_similarity_score[i],
                              round((paper_wise_ancestry_acc[i] / total_count[i]) * 100, 2),
                              round((paper_wise_ancestry_inc[i] / total_count[i]) * 100, 2),
                              round((paper_wise_bad_matches[i] / total_count[i]) * 100, 2),
                              paper_wise_extras[i],
                              total_count[i],
                              paper_wise_count_match_100[i],
                             ])
    length = len(total_count)
    paper_wise_df.append(['Overall',
                          ' - ',
                          sum(paper_wise_avg_similarity_score) / length,
                          round(sum(paper_wise_ancestry_acc) / sum(total_count) * 100, 2),
                          round(sum(paper_wise_ancestry_inc) / sum(total_count) * 100, 2),
                          round((paper_wise_bad_matches[i] / total_count[i]) * 100, 2), 
                          sum(paper_wise_extras),
                          sum(total_count),
                          sum(paper_wise_count_match_100),
                         ])  

    # Creating the comparing DataFrame
    comparison_df = pd.DataFrame(comparison_df, columns = ['PDF',
                                                           'Article',
                                                           'Name',
                                                           'Found_Name',
                                                           'Similarity_Score',
                                                           'Ancestry',
                                                           'Found_Ancestry'
                                                          ])
    paper_wise_df = pd.DataFrame(paper_wise_df, columns = ['PDF',
                                                             'Article',
                                                             'Average_Similarity_Score',
                                                             'Ancestry_Accuracy',
                                                             'Ancestry_Loss',
                                                             'Match_Not_Found',
                                                             'Extras_Found',
                                                             'Total_Cultures_Paper_Wise',
                                                             'Exact_Matches'
                                                            ])

    # Printing the final results
    print("Final Result")
    print("------------------------------------")
    print("Overall Similarity Score: " ,sum(paper_wise_avg_similarity_score) / length)
    print("Ancestry Accuracy: ", round(sum(paper_wise_ancestry_acc) / sum(total_count) * 100, 2), " %")
    print("Exact Matches: ", sum(paper_wise_count_match_100), " / ", sum(total_count))
    print("Good Matches Found: ", 100 - round(sum(paper_wise_bad_matches) / sum(total_count) * 100, 2), " %")
    return comparison_df, paper_wise_df

def visualize(paper_wise_df, images_dir, gpt):
    df = paper_wise_df.head(len(paper_wise_df) - 1)
    gpt_df = pd.read_csv(gpt)

    print("Visualizing")
    
    # Set a consistent style for all plots
    plt.style.use('seaborn-v0_8-whitegrid')

    # Plot line graph for Average Similarity Scores over different papers
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='PDF', y='Average_Similarity_Score', data=df, marker='o', ci='sd', linewidth=2, palette='deep')
    plt.title('Average Similarity Score Across Different Papers', fontsize=18, fontweight='bold')
    plt.xlabel('PDF', fontsize=14)
    plt.ylabel('Average Similarity Score', fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "average_similarity_score.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # This section generates a pie chart visualizing the distribution of ancestries obtained from web sources.
    ancestry_counts = gpt_df["Ancestry from web"].value_counts()
    ancestry_counts = ancestry_counts[ancestry_counts.index != "Not Reported"]  # Exclude "Not Reported" value
    plt.figure(figsize=(8, 8))
    plt.pie(ancestry_counts, labels=ancestry_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Ancestry from Web', fontsize=18, fontweight='bold')
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is a circle.
    plt.savefig(os.path.join(images_dir, "ancestry_distribution.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Prepare data for double bar graph
    total_counts = paper_wise_df['Total_Cultures_Paper_Wise']
    bad_matches = paper_wise_df['Match_Not_Found']

    # Create a DataFrame for plotting
    plot_data = pd.DataFrame({
        'Total Count': total_counts,
        'Bad Matches': bad_matches
    })

    # Plotting the double bar graph
    plt.figure(figsize=(12, 6))
    plot_data.plot(kind='bar', width=0.8)
    plt.title('Total Count vs Bad Matches', fontsize=18, fontweight='bold')
    plt.xlabel('Papers', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(ticks=range(len(paper_wise_df)), labels=paper_wise_df['PDF'], rotation=45)
    plt.legend(title='Metrics')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "total_count_vs_bad_matches.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Additional figures
    # Plot bar graph for Ancestry Accuracy
    plt.figure(figsize=(12, 6))
    sns.barplot(x='PDF', y='Ancestry_Accuracy', data=paper_wise_df, palette='pastel')
    plt.title('Ancestry Accuracy per Paper', fontsize=18, fontweight='bold')
    plt.xlabel('PDF', fontsize=14)
    plt.ylabel('Ancestry Accuracy (%)', fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "ancestry_accuracy_per_paper.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot line graph for Match Not Found percentage
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='PDF', y='Match_Not_Found', data=paper_wise_df, marker='o', ci='sd', linewidth=2, palette='muted')
    plt.title('Match Not Found Across Different Papers', fontsize=18, fontweight='bold')
    plt.xlabel('PDF', fontsize=14)
    plt.ylabel('Match Not Found Count', fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "match_not_found_per_paper.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot bar graph for Exact Matches
    plt.figure(figsize=(12, 6))
    sns.barplot(x='PDF', y='Exact_Matches', data=paper_wise_df, palette='viridis')
    plt.title('Exact Matches per Paper', fontsize=18, fontweight='bold')
    plt.xlabel('PDF', fontsize=14)
    plt.ylabel('Exact Matches', fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "exact_matches_per_paper.png"), dpi=300, bbox_inches='tight')
    plt.close()

    
    

    print("Images Saved to Images Folder.")

def main():
    args = parser.parse_args()
    print(args)
    
    # Create directory structure
    input_file_name = os.path.splitext(os.path.basename(args.gpt))[0]
    test_dir = os.path.join(args.output, input_file_name)
    csv_dir = os.path.join(test_dir, "csv")
    images_dir = os.path.join(test_dir, "images")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    # Redirect print output to a file
    log_file = os.path.join(test_dir, "test_output.txt")
    with open(log_file, 'w') as f:
        # Redirect stdout to the file
        import sys
        original_stdout = sys.stdout
        sys.stdout = f
        
        comparison_df, paper_wise_df = compare_csv(args.true, args.gpt, args.score)
        
        # Save CSV files
        comparison_df.to_csv(os.path.join(csv_dir, "Comparison.csv"), index=False)
        paper_wise_df.to_csv(os.path.join(csv_dir, "PaperWise.csv"), index=False)
        
        # Generate visualizations
        visualize(paper_wise_df, images_dir, args.gpt)
        
        # Restore stdout
        sys.stdout = original_stdout
    
    print(f"Test results saved in {test_dir}")
    print(f"CSV files saved in {csv_dir}")
    print(f"Images saved in {images_dir}")
    print(f"Test output log saved to {log_file}")

if __name__ == "__main__":
    main()


