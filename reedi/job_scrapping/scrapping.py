import requests
import json
import os
from os.path import join, dirname
import argparse
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def get_auth_endpoints_files(PATH_AUTH, PATH_ENDPOINTS):
    """
    Get the authentification and endpoints files

    Parameters
    ----------
    PATH_AUTH : str
        Path to the authentification file
    PATH_ENDPOINTS : str
        Path to the endpoints file

    Returns
    -------
    auth_file : dict
        Dictionary containing the authentification token
    endpoint_file : dict
        Dictionary containing the endpoints directions
    """
    print("PATH_AUTH", PATH_AUTH)
    print(join(PATH_AUTH, "theirstack_auth.json"))
    assert os.path.exists(
        join(PATH_AUTH, "theirstack_auth.json")
    ), "The path to the authentification file is not valid"
    assert os.path.exists(
        join(PATH_ENDPOINTS, "theirstack_endpoints.json")
    ), "The path to the endpoint file is not valid"

    with open(join(PATH_AUTH, "theirstack_auth.json"), "r") as f:
        auth_file = json.load(f)

    with open(join(PATH_ENDPOINTS, "theirstack_endpoints.json"), "r") as f:
        endpoint_file = json.load(f)

    return auth_file, endpoint_file


def get_compagny_scrapped(
    auth_file, endpoint_file, limit_compagny=500
):
    """
    Get the list of all the compagnies scrapped so far

    Parameters
    ----------
    auth_file : dict
        Dictionary containing the authentification token
    endpoint_file : dict
        Dictionary containing the endpoints directions
    compagny_id : int, optional
        Id of the compagny list, by default None
    limit_compagny : int, optional
        Number of compagny to get, by default 500

    Returns
    -------
    list
        List of the compagny scrapped
    """


    logging.info("Getting a predefined of all the compagnies")
    with open(join(dirname(__file__), "companies_list.txt"), "r") as f:
        compagnies = f.read().splitlines()

    TOKEN = auth_file["auth_token"]

    ENDPOINT = endpoint_file["compagny_lists_enpoint"]
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    companies_lists = requests.get(ENDPOINT, headers=headers)
    compagny_id = companies_lists.json()[0].get("id", 604)

    logging.info(f"Getting a list of compagnies from predfined list {compagny_id}")
    ENDPOINT = endpoint_file["compagny_endpoint"].format(compagny_id)
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    responses = requests.get(
        ENDPOINT, headers=headers, params={"page": 0, "limit": limit_compagny}
    )

    compagnies_extended = [response.get("company_name") for response in responses.json()]
    for compagny in compagnies_extended:
        compagny = compagny.strip()
        if compagny not in compagnies:
            compagnies.append(compagny)

    return compagnies


def get_job_parameters(PATH_JOB):
    """
    Get the job parameters

    Parameters
    ----------
    PATH_JOB : str
        Path to the job parameters file

    Returns
    -------
    job_parameters: dict
        Dictionary containing the job parameters
    """

    assert os.path.exists(
        join(PATH_JOB, "theirstack_job_config.json")
    ), "The path to the job parameters file is not valid"

    with open(join(PATH_JOB, "theirstack_job_config.json"), "r") as f:
        job_parameters = json.load(f)

    return job_parameters


def get_job_data(auth_file, endpoint_file, job_parameters, compagnies):
    """
    Get the data of a job

    Parameters
    ----------
    auth_file : dict
        Dictionary containing the authentification token
    endpoint_file : dict
        Dictionary containing the endpoints directions
    job_id : int
        Id of the job to get

    Returns
    -------
    dict
        Dictionary containing the data of the job
    """

    new_jobs = []

    TOKEN = auth_file["auth_token"]
    ENDPOINT = endpoint_file["job_endpoint"]
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

    for compagny in tqdm(compagnies):
        job_parameters["company_name_partial_match_or"] = [compagny.strip()]
        response = requests.post(ENDPOINT, headers=headers, json=job_parameters)
        try:
            new_jobs += response.json()["data"]
        except Exception as e:
            logging.info(e)
            continue
    return new_jobs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_auth", type=str, required=True, help="Path to the authentification file"
    )
    parser.add_argument(
        "--path_endpoints", type=str, required=True, help="Path to the endpoints file"
    )
    parser.add_argument(
        "--path_job", type=str, required=True, help="Path to the job parameters file"
    )
    parser.add_argument(
        "--path_output", type=str, required=True, help="Path to the output file"
    )
    parser.add_argument(
        "--start_date",
        type=str,
        required=True,
        help="Start date of the job",
    )
    parser.add_argument(
        "--end_date",
        type=str,
        required=True,
        help="End date of the job",
    )
    parser.add_argument(
        "--limit_compagny",
        type=int,
        required=False,
        default=500,
        help="Number of compagny to get",
    )
    parser.add_argument(
        "--f",
        type=bool,
        required=False,
        default=False,
        help="Force the scrapping even if the data already exists",
    )

    args = parser.parse_args()

    PATH_AUTH = args.path_auth
    PATH_ENDPOINTS = args.path_endpoints
    PATH_JOB = args.path_job
    PATH_OUTPUT = args.path_output
    start_date = args.start_date
    end_date = args.end_date

    logging.info("Getting authentification and endpoints files")

    auth_file, endpoint_file = get_auth_endpoints_files(PATH_AUTH, PATH_ENDPOINTS)

    job_parameters = get_job_parameters(PATH_JOB)
    job_parameters["posted_at_gte"] = start_date
    job_parameters["posted_at_lte"] = end_date

    if not os.path.isdir(PATH_OUTPUT):
        os.mkdir(PATH_OUTPUT)

    if not os.path.isdir(join(PATH_OUTPUT, f"{start_date}_{end_date}")):
        os.mkdir(join(PATH_OUTPUT, f"{start_date}_{end_date}"))

    if not args.f and os.path.exists(
        join(PATH_OUTPUT, f"{start_date}_{end_date}", "job_data.json")
    ):
        logging.info(f"The data of {start_date} to {end_date} already exists")
        exit()

    logging.info("Getting compagnies list")

    compagnies = get_compagny_scrapped(
        auth_file,
        endpoint_file,
        limit_compagny=args.limit_compagny,
    )

    logging.info("Getting the data of a job")

    jobs = get_job_data(auth_file, endpoint_file, job_parameters, compagnies)

    logging.info(f"Saving the data of {len(jobs)} jobs")

    with open(join(PATH_OUTPUT, f"{start_date}_{end_date}", "job_data.json"), "w") as f:
        json.dump(jobs, f)
