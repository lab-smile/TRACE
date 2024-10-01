import argparse
import os
import pandas as pd
from PyPDF2 import PdfReader
import re

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default = "", type = str,  help = "File Path for Individual mode")
parser.add_argument("-p", "--papers", default = "/blue/ruogu.fang/chintan.acharya/smile-lab/Ancestry/RegexAndChatgpt/papers/Science_of_Translational_Medicine", type = str, help = "Directory of Journals")

def main():
    args = parser.parse_args()
    process(args.file, args.papers)

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf = PdfReader(file)
        text = " ".join([page.extract_text() for page in pdf.pages])
    return text

def process(fileName, directory):
    if fileName[-4:] == ".csv":
        print("Reading CSV")
        df = pd.read_csv(fileName)
        rows = []
        for paper in list(df['File Id'].unique()):
            print(f"Starting {paper}")
            text = extract_text_from_pdf(os.path.join(directory, paper))
            print(f"Reading {paper} complete.")
            for index, row in df[df['File Id'] == paper].iterrows():
                match = re.search(re.escape(row['Name']), text)
                if match:
                    pass
                else:
                    rows.append(index)
            print(f"{paper} done.")
            print()
        updated_df = df.drop(rows)
        updated_df.to_csv(f"{fileName[0:-4]}_updated.csv")
        print(f"{fileName} updated to {fileName[0:-4]}_updated.csv")
    else:
        print("Only CSV files allowed")

if __name__ == "__main__":
    main()
