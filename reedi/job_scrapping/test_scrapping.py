import json
import pytest
import requests_mock

from scrapping import (
    get_auth_endpoints_files,
    get_compagny_scrapped,
    get_job_parameters,
    get_job_data,
)


def test_get_auth_endpoints_files(tmpdir):
    # Create temporary auth and endpoints files
    auth_file = tmpdir.mkdir("auth").join("theirstack_auth.json")
    auth_file.write(json.dumps({"token": "1234"}))

    endpoint_file = tmpdir.mkdir("endpoints").join("theirstack_endpoints.json")
    endpoint_file.write(json.dumps({"url": "http://example.com"}))

    # Call the function with the paths to the temporary files
    auth, endpoints = get_auth_endpoints_files(
        str(auth_file.dirname), str(endpoint_file.dirname)
    )

    # Check that the function correctly read the files
    assert auth == {"token": "1234"}
    assert endpoints == {"url": "http://example.com"}

    # Check that the function raises an assertion error if the files do not exist
    with pytest.raises(AssertionError):
        get_auth_endpoints_files("/nonexistent/path", "/nonexistent/path")


def test_get_compagny_scrapped():
    auth_file = {"auth_token": "test_token"}
    endpoint_file = {
        "compagny_lists_enpoint": "http://example.com/lists",
        "compagny_endpoint": "http://example.com/compagnies/{}",
    }

    with requests_mock.Mocker() as m:
        m.get("http://example.com/lists", json=[{"id": 1}])
        m.get(
            "http://example.com/compagnies/1", json=[{"company_name": "Test Company"}]
        )

        companies = get_compagny_scrapped(auth_file, endpoint_file)

    assert companies == ["Test Company"]


def test_get_job_parameters(tmpdir):
    # Create temporary job parameters file
    job_file = tmpdir.mkdir("job").join("theirstack_job_config.json")
    job_file.write(json.dumps({"param1": "value1"}))

    # Call the function with the path to the temporary file
    job_parameters = get_job_parameters(str(job_file.dirname))

    # Check that the function correctly read the file
    assert job_parameters == {"param1": "value1"}

    # Check that the function raises an assertion error if the file does not exist
    with pytest.raises(AssertionError):
        get_job_parameters("/nonexistent/path")


def test_get_job_data():
    auth_file = {"auth_token": "test_token"}
    endpoint_file = {"job_endpoint": "http://example.com/jobs"}
    job_parameters = {"param1": "value1"}
    companies = ["Test Company"]

    with requests_mock.Mocker() as m:
        m.post("http://example.com/jobs", json={"data": [{"job": "Test Job"}]})

        jobs = get_job_data(auth_file, endpoint_file, job_parameters, companies)

    assert jobs == [{"job": "Test Job"}]
