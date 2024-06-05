import pandas as pd
from ojd_daps_skills.pipeline.extract_skills.extract_skills import ExtractSkills
from os.path import join, dirname
import argparse
import logging

logging.basicConfig(level=logging.INFO)


def load_file(file_name):
    """Parameters
    ----------
    file_name : str
        Name of input CSV file"""

    logging.info(f"Loading file: {file_name}")
    return pd.read_csv(file_name)


def save_file(dataframe, file_name):
    """Parameters
    ----------
    dataframe : pandas dataframe of skills
    file_name : str
        Name of output CSV file"""

    logging.info(f"Saving file: {file_name}")
    dataframe.to_csv(file_name, index=False)


def separate_skills(skills, skill_type="extracted"):
    """
    Seperates the extracted skill, mapped skill, and reference of mapped skill from the dictionary output.
      example :
        {'SKILL': [('problem solving', ('problem solve', '334e3e49-fb02-4051-809a-f06adfdc1c40')),
         ('Time Management', ('managing time', 'd9013e0e-e937-43d5-ab71-0e917ee882b8')),
         ('Organisational Skills', ('management skills', 'S4.0.0'))]}
    """
    separated_skill = []  # saves the seperates values of loop

    for i in skills.values():  # loops through list of tuples (value of the key'SKILL')
        for (
            a
        ) in (
            i
        ):  # loops tuples (one tuple for each skill with 3 values (extracted, mapped, reference))
            if skill_type == "extracted":
                separated_skill.append(a[0])  # tuple first value is extracted skill
            elif skill_type == "mapped":
                separated_skill.append(
                    a[1][0]
                )  # (selects inside tuple[1] value[0], mapped skill)
            elif skill_type == "reference":
                separated_skill.append(
                    a[1][-1]
                )  # (selects inside tuple[1] value[-1], last value which is reference)

    return separated_skill


def main():
    logging.info("Starting Skill Extraction")

    parser = argparse.ArgumentParser(description="Process input and output file paths.")
    parser.add_argument(
        "--input_file_path", type=str, required=True, help="Path to the input CSV file."
    )
    parser.add_argument(
        "--output_file_path",
        type=str,
        required=True,
        help="Path to the output CSV file.",
    )

    args = parser.parse_args()

    input_file_path = args.input_file_path
    output_file_path = args.output_file_path

    # Load CSV file
    df = load_file(input_file_path)

    # Instantiate ExtractSkills
    es_esco = ExtractSkills(config_name="extract_skills_esco", local=True)

    # Load taxonomy
    es_esco.load()
    logging.info("Taxonomy loaded successfully.")

    # Extract skills from the description column (or change it with your column name if different in the input file)

    matched_dfs = []

    for i in range(0, len(df), 500):
        df_matched = df.iloc[i:i+500]
        df_matched["Skills_Matched_ESCO"] = es_esco.extract_skills(df_matched["description"])
        matched_dfs.append(df_matched)

    df = pd.concat(matched_dfs)

    df["Skills_Extracted"] = df["Skills_Matched_ESCO"].apply(
        lambda x: separate_skills(
            x, skill_type="extracted"
        )  # apply function on df column to get values
    )
    df["Skills_Mapped_ESCO"] = df["Skills_Matched_ESCO"].apply(
        lambda x: separate_skills(
            x, skill_type="mapped"
        )  # apply function on df column to get values
    )
    df["Skills_Mapped_ESCO_Refrence"] = df["Skills_Matched_ESCO"].apply(
        lambda x: separate_skills(
            x, skill_type="reference"
        )  # apply function on df column to get values
    )

    # Explode the DataFrame to separate skills into individual rows
    df = df.explode(
        ["Skills_Extracted", "Skills_Mapped_ESCO", "Skills_Mapped_ESCO_Refrence"]
    ).reset_index(drop=True)

    # Save separated skills to CSV
    save_file(df, output_file_path)

    logging.info("Skills Extraction completed successfully.")


if __name__ == "__main__":
    main()
