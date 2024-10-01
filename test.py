from testhelper.helper import dict1, dict2, similar, remove_spaces, convert_string_to_df
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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
parser.add_argument("-s", "--score", default=50.0, type=float, help="Similarity score threshold")
parser.add_argument("-p", "--prefix", type=str, help="Prefix of file Names")
parser.add_argument("-o", "--output", default="", type=str, help="Output directory for test results", required=True)

def compare_csv(true_csv, gpto_csv, prefix, sim_score_thresh = 50.0):
    print("Starting Comparison.")
    true_df = pd.read_csv(true_csv)
    gpto_df = pd.read_csv(gpto_csv)

    true_df.columns = ['Name', 'Ancestry', 'Lines with Ancestry', 'Type', 'Supplier', 'Articles', 'Primary/Line', 'Notes', 'Body Part/Tissue', 'URL', 'Flag', 'Journal', 'flag']
    true_df = true_df.drop(columns = ['Lines with Ancestry', 'Type', 'Supplier', 'Notes', 'Body Part/Tissue', 'URL', 'Flag', 'flag'])

    gpto_df = gpto_df.drop(columns = ['Gender', 'Age', 'Category'])
    true_df = true_df[true_df['Journal'] == 'https://www.notion.so/f3f7e3cf261449c3b4b8885d49aab57d']
    gpto_df = gpto_df.fillna('')

    true_dict = defaultdict(lambda : [])
    count = 0
    for article in list(true_df['Articles'].unique()):
        for index, row in true_df[true_df['Articles'] == article].iterrows():
            try:
                true_dict[dict2[row['Articles']]].append((index, row['Name'], row['Ancestry']))
            except KeyError:
                break

    gpto_dict = defaultdict(lambda : [])
    for fid in list(gpto_df['File Id'].unique()):
        if dict1[int(fid[0:-4])] != "":
            count = 0
            for index, row in gpto_df[gpto_df['File Id'] == fid].iterrows():
                gpto_dict[int(fid[0:-4])].append((index, row['Name'], row['Ancestry Reported'], row['Ancestry Available'], row['Ancestry from Web']))
    

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

    paper_wise_avg_similarity_score = []
    paper_wise_ancestry_acc = []
    paper_wise_ancestry_inc = []
    paper_wise_count_match_25 = []
    paper_wise_count_match_50 = []
    paper_wise_count_match_75 = []
    paper_wise_count_match_100 = []
    special_cases = []
    paper_wise_reported_corr = []
    paper_wise_reported_inco = []
    paper_wise_available_corr = []
    paper_wise_available_inco = []
    total_count = []
    comparison_df = []

    for i in papers:
        paper_avg_sim_score = 0
        paper_ancestry_acc = 0
        paper_ancestry_inc = 0
        paper_reported_corr = 0
        paper_reported_inco = 0
        paper_count_match_25 = 0
        paper_count_match_50 = 0
        paper_count_match_75 = 0
        paper_count_match_100 = 0

        if true_dict[i] and gpto_dict[i]:
            for true_row in true_dict[i]:
                max_sim_score = -1
                max_sim_row = ()

                for gpto_row in gpto_dict[i]:
                    sim_score = (similar(gpto_row[1], true_row[1]) * 100)
                    if max_sim_score < sim_score:
                        max_sim_score = sim_score 
                        max_sim_row = gpto_row
                
                paper_avg_sim_score += max_sim_score

                if max_sim_score >= 25.0:
                    paper_count_match_25 += 1
                if max_sim_score >= 50.0:
                    paper_count_match_50 += 1
                if max_sim_score >= 75.0:
                    paper_count_match_75 += 1
                if max_sim_score == 100.0:
                    paper_count_match_100 += 1

                if true_row[-1] == 'Not Reported':
                    if max_sim_row[2]:
                        paper_reported_inco += 1
                    else:
                        paper_reported_corr += 1
                    if max_sim_row[-1] == 'Not Available' or max_sim_row[-1] == '':
                        paper_ancestry_acc += 1
                    else:
                        paper_ancestry_inc += 1
                        special_cases.append([max_sim_row, true_row])
                else:
                    if max_sim_row[2]:
                        paper_reported_corr += 1
                    else:
                        paper_reported_inco += 1
                    if max_sim_row == 'Not Available' or max_sim_row == '':
                        paper_ancestry_inc += 1
                    else:
                        if len(max_sim_row[-1].split('\n')) > 1:
                            origin = convert_string_to_df(max_sim_row[-1]).head(1)
                            origin = list(origin['Origin'])[0]
                            if origin.split(',')[0] == true_row[-1].split(',')[0]:
                                paper_ancestry_acc += 1
                            else:
                                paper_ancestry_inc += 1
                        else:
                            if max_sim_row[-1] == true_row[-1]:
                                paper_ancestry_acc += 1
                            else:
                                paper_ancestry_inc += 1

                if max_sim_score >= 50.0:
                    comparison_df.append([str(i) + '.pdf', 
                                          dict1[i], 
                                          true_row[1], 
                                          max_sim_row[1], 
                                          round(max_sim_score, 2), 
                                          true_row[-1], 
                                          max_sim_row[-1]
                                         ])
                else:
                    comparison_df.append([str(i) + '.pdf',
                                          dict1[i], 
                                          true_row[1], 
                                          "No good match Found", 
                                          0, 
                                          true_row[-1], 
                                          "N/A"
                                         ])

        paper_wise_avg_similarity_score.append(paper_avg_sim_score / len(true_dict[i]))
        paper_wise_ancestry_acc.append(paper_ancestry_acc)
        paper_wise_ancestry_inc.append(paper_ancestry_inc)
        paper_wise_count_match_25.append(paper_count_match_25)
        paper_wise_count_match_50.append(paper_count_match_50)
        paper_wise_count_match_75.append(paper_count_match_75)
        paper_wise_count_match_100.append(paper_count_match_100)
        paper_wise_reported_corr.append(paper_reported_corr)
        paper_wise_reported_inco.append(paper_reported_inco)
        total_count.append(len(true_dict[i]))

    paper_wise_df = []
    for i in range(len(papers)):
        paper_wise_df.append([str(papers[i]) + '.pdf',
                              dict1[papers[i]],
                              paper_wise_avg_similarity_score[i],
                              round((paper_wise_ancestry_acc[i] / total_count[i]) * 100, 2),
                              round((paper_wise_ancestry_inc[i] / total_count[i]) * 100, 2),
                              round((paper_wise_reported_corr[i] / total_count[i]) * 100, 2),
                              round((paper_wise_reported_inco[i] / total_count[i]) * 100, 2),
                              total_count[i],
                              paper_wise_count_match_25[i],
                              paper_wise_count_match_50[i],
                              paper_wise_count_match_75[i],
                              paper_wise_count_match_100[i],
                             ])
    length = len(total_count)
    paper_wise_df.append(['Overall',
                          ' - ',
                          sum(paper_wise_avg_similarity_score) / length,
                          round(sum(paper_wise_ancestry_acc) / sum(total_count) * 100, 2),
                          round(sum(paper_wise_ancestry_inc) / sum(total_count) * 100, 2),
                          round(sum(paper_wise_reported_corr) / sum(total_count) * 100, 2),
                          round(sum(paper_wise_reported_inco) / sum(total_count) * 100, 2),
                          sum(total_count),
                          sum(paper_wise_count_match_25),
                          sum(paper_wise_count_match_50),
                          sum(paper_wise_count_match_75),
                          sum(paper_wise_count_match_100),
                         ])  

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
                                                             'Ancestry_Reported_Decision_Accuracy',
                                                             'Ancestry_Reported_Decision_Loss',
                                                             'Total_Cultures_Paper_Wise',
                                                             'Matches_Found_Paper_Wise_With_Similarity_Score_25',
                                                             'Matches_Found_Paper_Wise_With_Similarity_Score_50',
                                                             'Matches_Found_Paper_Wise_With_Similarity_Score_75',
                                                             'Matches_Found_Paper_Wise_With_Similarity_Score_100'
                                                            ])

    print(f"Comparison Completed, saved to {prefix}Comparison.csv and {prefix}PaperWise.csv")
    print("Final Result")
    print("------------------------------------")
    print("Overall Similarity Score: " ,sum(paper_wise_avg_similarity_score) / length)
    print("Ancestry Accuracy: ", round(sum(paper_wise_ancestry_acc) / sum(total_count) * 100, 2), " %")
    print("Ancestry Reported Boolean Accuracy: ", round(sum(paper_wise_reported_corr) / sum(total_count) * 100, 2), " %")
    print("Ancestry Reported Loss: ", round(sum(paper_wise_reported_inco) / sum(total_count) * 100, 2), " %")
    print("Cell Lines with more than 25 similarity Scores: ", sum(paper_wise_count_match_25), " / ", sum(total_count))
    print("Cell Lines with more than 50 similarity Scores: ", sum(paper_wise_count_match_50), " / ", sum(total_count))
    print("Cell Lines with more than 75 similarity Scores: ", sum(paper_wise_count_match_75), " / ", sum(total_count))
    print("Cell Lines with more than 100 similarity Scores: ", sum(paper_wise_count_match_100), " / ", sum(total_count))
    return comparison_df, paper_wise_df

def visualize(paper_wise_df, images_dir):
    df = paper_wise_df.head(len(paper_wise_df) - 1)

    print("Visualizing")
    
    # Set a consistent style for all plots
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Plot Average Similarity Scores
    plt.figure(figsize=(12, 7))
    sns.histplot(df['Average_Similarity_Score'], bins=20, kde=True, color='skyblue')
    plt.title('Distribution of Average Similarity Scores', fontsize=18, fontweight='bold')
    plt.xlabel('Average Similarity Score', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.savefig(os.path.join(images_dir, "average_similarity_score_distribution.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot Ancestry Accuracy and Loss
    plt.figure(figsize=(12, 7))
    sns.boxplot(data=df[['Ancestry_Accuracy', 'Ancestry_Loss', 'Ancestry_Reported_Decision_Accuracy', 'Ancestry_Reported_Decision_Loss']], palette='Set3')
    plt.title('Ancestry Accuracy and Loss Metrics', fontsize=18, fontweight='bold')
    plt.ylabel('Percentage', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.savefig(os.path.join(images_dir, "ancestry_accuracy_and_loss.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Stacked bar plot for matches found
    plt.figure(figsize=(14, 8))
    df.plot(x='PDF', y=['Matches_Found_Paper_Wise_With_Similarity_Score_25', 'Matches_Found_Paper_Wise_With_Similarity_Score_50', 'Matches_Found_Paper_Wise_With_Similarity_Score_75', 'Matches_Found_Paper_Wise_With_Similarity_Score_100'], kind='bar', stacked=True, colormap='viridis')
    plt.title('Matches Found Paper-Wise with Different Similarity Scores', fontsize=18, fontweight='bold')
    plt.xlabel('PDF', fontsize=14)
    plt.ylabel('Number of Matches Found', fontsize=14)
    plt.legend(fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "matches_found_paper_wise.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Scatter plot to visualize Ancestry_Accuracy vs. Average_Similarity_Score
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(x='Average_Similarity_Score', y='Ancestry_Accuracy', data=df, hue='Total_Cultures_Paper_Wise', palette='viridis', size='Total_Cultures_Paper_Wise', sizes=(20, 200))
    plt.title('Ancestry Accuracy vs. Average Similarity Score', fontsize=18, fontweight='bold')
    plt.xlabel('Average Similarity Score', fontsize=14)
    plt.ylabel('Ancestry Accuracy', fontsize=14)
    plt.legend(title='Total Cultures', title_fontsize='13', fontsize='11', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "ancestry_accuracy_vs_similarity_score.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot line graph for Average Similarity Scores over different papers
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='PDF', y='Average_Similarity_Score', data=df, marker='o')
    plt.title('Average Similarity Score Across Different Papers', fontsize=18, fontweight='bold')
    plt.xlabel('PDF', fontsize=14)
    plt.ylabel('Average Similarity Score', fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "average_similarity_score.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot line graph for Ancestry Accuracy and Ancestry Reported Decision Accuracy
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='PDF', y='Ancestry_Accuracy', data=df, marker='o', label='Ancestry Accuracy')
    sns.lineplot(x='PDF', y='Ancestry_Reported_Decision_Accuracy', data=df, marker='s', label='Reported Decision Accuracy')
    plt.title('Ancestry and Reported Decision Accuracy Across Different Papers', fontsize=18, fontweight='bold')
    plt.xlabel('PDF', fontsize=14)
    plt.ylabel('Accuracy (%)', fontsize=14)
    plt.xticks(rotation=90)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'ancestry_accuracy_decision_accuracy.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot line graph for Ancestry Loss and Ancestry Reported Decision Loss
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='PDF', y='Ancestry_Loss', data=df, marker='o', label='Ancestry Loss')
    sns.lineplot(x='PDF', y='Ancestry_Reported_Decision_Loss', data=df, marker='s', label='Reported Decision Loss')
    plt.title('Ancestry and Reported Decision Loss Across Different Papers', fontsize=18, fontweight='bold')
    plt.xlabel('PDF', fontsize=14)
    plt.ylabel('Loss (%)', fontsize=14)
    plt.xticks(rotation=90)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "ancestry_loss_decision_loss.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # Line graph to visualize Matches Found with Different Similarity Scores
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='PDF', y='Matches_Found_Paper_Wise_With_Similarity_Score_25', data=df, marker='o', label='Similarity Score 25')
    sns.lineplot(x='PDF', y='Matches_Found_Paper_Wise_With_Similarity_Score_50', data=df, marker='s', label='Similarity Score 50')
    sns.lineplot(x='PDF', y='Matches_Found_Paper_Wise_With_Similarity_Score_75', data=df, marker='^', label='Similarity Score 75')
    sns.lineplot(x='PDF', y='Matches_Found_Paper_Wise_With_Similarity_Score_100', data=df, marker='D', label='Similarity Score 100')
    plt.title('Matches Found with Different Similarity Scores Across Papers', fontsize=18, fontweight='bold')
    plt.xlabel('PDF', fontsize=14)
    plt.ylabel('Matches Found', fontsize=14)
    plt.xticks(rotation=90)
    plt.legend(fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "matches_found_similarity_scores.png"), dpi=300, bbox_inches='tight')
    plt.close()

    print("Images Saved to Images Folder.")

def main():
    args = parser.parse_args()
    
    # Create directory structure
    input_file_name = os.path.splitext(os.path.basename(args.gpt))[0]
    test_dir = os.path.join(args.output, input_file_name)
    csv_dir = os.path.join(test_dir, "csv")
    images_dir = os.path.join(test_dir, "images")
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    # Redirect print output to a file
    log_file = os.path.join(test_dir, "test_output.txt")
    with open(log_file, 'w') as f:
        # Redirect stdout to the file
        import sys
        original_stdout = sys.stdout
        sys.stdout = f
        
        comparison_df, paper_wise_df = compare_csv(args.true, args.gpt, args.prefix, args.score)
        
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


