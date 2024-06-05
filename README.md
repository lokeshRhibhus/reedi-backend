# REEDI Project

This repository contains the REEDI project. Here are the steps to set up the environment and get started.

## Table of contents:

- [:gear: Setup](#setup)
- [:hook: Job Scrapping](#job-scrapping)
- [:mag_right: Skill Extraction and Classification](#skill-extraction-and-classification)


## Prerequisites

- Python 3.10
- Git
- DVC

## :gear: Setup

1. **Clone and navigate to the repository**

    Use the following command to clone the repository:

    ```bash
    git clone <repository-url>
    ```

    Navigite to repo directory:

    ```bash
    cd <repository-directory>
    ```

2. **Create and activate a virtual environment**

    Install virtual invironment library:

    ```bash
    pip install virtualenv

    ```

    Create virtual environment:

    ```bash
    python3.10 -m venv <environment-name>

    ```

    Activate virtual environment:

    ```bash
    source <environment-name>/bin/activate

    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure pre-commit**

    Pre-commit is a tool that runs checks on your code before you commit it. It is configured in the `.pre-commit-config.yaml` file. To install it, run the following command:

    ```bash
    pip install pre-commit
    ```

5. **DVC management**

    DVC is a tool for data versioning. To get the data from the remote storage, run the following command:

    ```bash
    dvc pull
    ```


You are now ready to start working on the REEDI project!


## :hook: Job Scrapping

### Main objective

This Python script is    to scrape job data from a specific source. It uses authentication tokens and endpoint directions to fetch data about companies and their jobs. The script takes in a date range (defined by environment variables `START_DATE` and `END_DATE`) and fetches job data posted within this range. The scraped data is then saved in a JSON file in a directory named after the date range.

### :snake: How to run the script with the command line

With the script `reedi/job_scrapping/scrapping.py`, you can scrapper data from Indeed or LinkedIn and save it in `data/raw/jobs/`.

1. **Run the script**

    Run the script with the following command:

    ```bash
    python scrapping.py --path_auth <path_to_auth_file> --path_endpoints <path_to_endpoints_file> --path_job <path_to_job_parameters_file> --path_output <path_to_output_directory> [--id <compagny_list_id>] [--limit_compagny <number_of_companies>] [--f <force_scrapping>]]  --start_date <start_date> --end_date <end_date>
    ```

    Replace the following arguments with the appropriate paths:
    - `<path_to_auth_file>`: Path to the authentication file. This file contains the authentication tokens required to fetch data.
    - `<path_to_endpoints_file>`: Path to the endpoints file. This file contains the endpoints required to fetch data.
    - `<path_to_job_parameters_file>`: Path to the job parameters file. This file contains the parameters required to fetch data.
    - `<path_to_output_directory>`: Path to the output directory. This is where the scraped data will be saved.
    - `<compagny_list_id>`: ID of the list of companies to scrape data from. If not specified, the script will scrape data from all companies (limited to 300).
    - `--f`: Force scrapping. If specified, the script will scrape data even if the output directory already exists.
    - `<start_date>`: Start date of the date range to scrape data from. Format: `YYYY-MM-DD`.
    - `<end_date>`: End date of the date range to scrape data from. Format: `YYYY-MM-DD`.

2. **Example of command**

    ```bash
    python scrapping.py --path_auth auth.json --path_endpoints endpoints.json --path_job job_parameters.json --path_output output --id 999 --limit_compagny 10 --f
    ```

    This command will scrape data from the 10 first companies of the list with ID `999` and save the data in the `output` directory. If the `output` directory already exists, the script will scrape data anyway.


## :🔎: Skill Extraction and Classification 
### Main Objective
This Python script is designed to extract and map skills from the given data based on a pre-defined taxonomy(ESCO). It takes in a CSV file as input and produces a CSV output file with extracted and mapped skills. The column name containing the main text to be processed needs to be changed to apply the extraction and mapping function in the `skills_extractor.py`.

### How to run the script with the command line
With the script `reedi/skill_extracting/skills_extractor.py`, you can extract skills from the input file and save the output file in the given directory.

1. Usage:
- Run the script with the following command:
```bash
python skills_extractor.py --input_file_path <input_file_path> --output_file_path <output_file_path>
```

Replace the following arguments with the appropriate paths:
- `<input_file_path>`: Path to the input file in CSV format.
- `<output_file_path>`: Assign a name and path to the output file in CSV format.

2. Example of command
```bash
python skills_extractor.py --input_file_path data.csv --output_file_path data_skills.csv
```
This command will extract skills from the data.csv file and save the data_skills.csv in the given output directory.


## Run end to end

To run the pipeline end to end, use the following command:
```bash
bash ./run_pipeline.sh
```
