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


