#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

start_date=$(date -d "`date +%Y%m01` -1 month" +%Y-%m-%d)
end_date=$(date -d "`date +%Y%m01` -1 day" +%Y-%m-%d)

echo -e "${YELLOW}getting data...${NC}"
dvc pull
echo -e "${GREEN}finished getting data.${NC}"

echo -e "${YELLOW}getting jobs...${NC}"
python ./reedi/job_scrapping/scrapping.py \
        --path_auth reedi/job_scrapping/ \
        --path_endpoints reedi/job_scrapping/ \
        --path_job reedi/job_scrapping/ \
        --path_output data/raw/jobs/ \
        --start_date ${start_date} \
        --end_date ${end_date} \
        --f F
echo -e "${GREEN}finished getting jobs.${NC}"

echo -e "${YELLOW}cleaning_jobs data...${NC}"
python ./reedi/scripts/parse_raw_jobs.py \
		--input_folder_path data/raw/jobs/ \
		--output_file_path data/processed/jobs_clean/NEW_IR_Companies_Clean.csv
echo -e "${GREEN}finished cleaning jobs.${NC}"

echo -e "${YELLOW}extracting and matching skills...${NC}"
python ./reedi/skill_extracting/skills_extractor.py \
      --input_file_path data/processed/jobs_clean/NEW_IR_Companies_Clean.csv \
      --output_file_path data/processed/jobs_extracted/NEW_IR_Companies_Extracted.csv
echo -e "${GREEN}finished extracting and matching skills.${NC}"

echo -e "${YELLOW}committing to dvc...${NC}"
dvc add data/raw/
dvc add data/processed/
echo -e "${GREEN}finished committing to dvc.${NC}"

echo -e "${YELLOW}pushing to dvc...${NC}"
dvc push
echo -e "${GREEN}finished pushing to dvc.${NC}"

echo -e "${YELLOW}adding changes to git...${NC}"
git add .
echo -e "${GREEN}finished adding to git.${NC}"

echo -e "${YELLOW}committing to git...${NC}"
git commit -m "Updating data for period ${start_date}-${end_date}"
echo -e "${GREEN}finished committing to git.${NC}"

echo -e "${YELLOW}pushing to git...${NC}"
git push
echo -e "${GREEN}finished pushing to git.${NC}"

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
