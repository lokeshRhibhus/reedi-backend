import pandas as pd
from skills_extractor import load_file, save_file, main
import pytest
import argparse


@pytest.fixture
def sample_dataframe():  # creates a samle dataframe
    data = {"Description": ["Description 1", "Description 2"]}
    return pd.DataFrame(data)


def test_load_file(tmp_path, sample_dataframe):  # loads a test file
    file_path = tmp_path / "test_input.csv"
    sample_dataframe.to_csv(file_path, index=False)
    result_df = load_file(tmp_path, "test_input.csv")
    assert result_df.equals(sample_dataframe)


def test_save_file(tmp_path, sample_dataframe):  # saves the output file as test
    file_path = tmp_path / "test_output.csv"
    save_file(sample_dataframe, tmp_path, "test_output.csv")
    result_df = pd.read_csv(file_path)
    assert result_df.equals(sample_dataframe)


def test_main(
    tmp_path, capsys, sample_dataframe, monkeypatch
):  # tests the main function by taking path and dataframe
    file_path = tmp_path / "test_input.csv"
    output_file_path = tmp_path / "test_output.csv"
    sample_dataframe.to_csv(file_path, index=False)

    # Create an argparse.ArgumentParser object to simulate command line arguments
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

    # Set the required command-line arguments using monkeypatch
    monkeypatch.setattr(
        "sys.argv",
        [
            "skills_extractor.py",
            "--input_file_path",
            str(file_path),
            "--output_file_path",
            str(output_file_path),
        ],
    )

    # Call the main function
    main()

    captured = capsys.readouterr()
    assert "Usage:" not in captured.out
    assert output_file_path.exists()
