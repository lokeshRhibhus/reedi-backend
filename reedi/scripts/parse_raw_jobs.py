import pandas as pd
from os.path import join, dirname
import argparse
import logging
import json
import tqdm
import os
import glob


def get_clean_jobs(infile):

    df = pd.read_json(infile)

    cols_rmv = [
        "countries",
        "cities",
        "min_annual_salary_usd",
        "min_annual_salary",
        "max_annual_salary",
        "max_annual_salary_usd",
        "avg_annual_salary_usd",
        "salary_currency",
        "country",
        "continents",
        "salary_string",
        "matching_phrases",
        "matching_words",
        "manager_roles",
        "company_object",
        "hiring_team",
        "country_code",
        "country_codes",
        "seniority"
    ]

    df = df.drop(cols_rmv, axis=1)

    ignore_companies = [
        "Workday",
        "IBM",
        "Microsoft",
        "Apple",
        "TikTok",
        "Bank of Ireland",
        "Accenture",
        "Digiweb",
        "FLYING COLOURS CONSULTANCY LIMITED",
        "Spector Information Security Limited."
    ]

    ignore_titles = [
        "software engineer",
        "senior software engineer"
    ]

    df = df[~df.normalized_title.isin(ignore_titles)]

    df = df[~df.company.isin(ignore_companies)]

    df = df.dropna()

    df.drop_duplicates(keep='last', inplace=True)

    return df

def main():
    logging.info("Creating clean jobs file")

    parser = argparse.ArgumentParser(description="Process input and output paths.")
    parser.add_argument(
        "--input_folder_path",
        type=str,
        required=True,
        help="Path to the input json jobs folder."
    )
    parser.add_argument(
        "--output_file_path",
        type=str,
        required=True,
        help="Path to the output CSV file.",
    )

    args = parser.parse_args()

    input_folder_path = args.input_folder_path
    output_file_path = args.output_file_path

    if os.path.isdir(input_folder_path):
        infiles = []
        for root, dirs, files in os.walk(input_folder_path):
            for f in files:
                if f.endswith('.json'):
                    infiles.append(os.path.join(root, f))

        dfs = []
        for file in tqdm.tqdm(infiles):
            df = get_clean_jobs(file)
            dfs.append(df)

        concat_dfs = pd.concat(dfs)

        # write CSV file
        concat_dfs.to_csv(output_file_path)
    else:
        raise FileNotFoundError

if __name__ == "__main__":
    main()
