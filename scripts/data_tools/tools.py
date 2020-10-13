# Developed and tested in Python 3.8.6-amd64 on Windows
import csv
import os
from . import election


def read_list_from_file(file_path):
    """
    Reads file_path, returning a list lines in the file.

    :param file_path: The file to read lines from.
    :return: list: A list of strings that correspond to each line in the file.
    """
    file_contents = None
    with open(file_path) as f:
        file_contents = f.readlines()

    return [item.rstrip() for item in file_contents]


def write_list_to_file(contents, file_path):
    """
    Writes a list to a text file, placing each list element on its own line.

    :param contents: The list to write to the file.
    :param file_path: The file that should be written to
    """
    file_contents = None
    with open(file_path, 'w') as outfile:
        for item in contents:
            outfile.write(item)
            outfile.write("\n")



def get_files_in_folder(folder_path):
    """
    Returns a list of all files in a given folder. Does not return folder names. Does not recurse into
    subdirectories.

    :param folder_path: The folder to search for files in.
    :return: list: A list of each filename in that folder
    """
    files_list = []
    for f in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, f)):
            files_list.append(os.path.join(folder_path, f))

    return files_list


def load_data_file(file_path):
    """
    Loads a csv file, creating one Election object for each row, and returning a list of all the Election objects
    found in the file. This function expects the file to be in a specific format, see the accompanying CSV files
    for examples.

    :param file_path: Path to the csv file that should be loaded
    :return: list: List of Election objects containing election data.
    """
    elections = []
    csv_data = []
    with open(file_path) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csv_data.append(row)

    for row in csv_data[1:]:
        new_election = election.Election(row[0], row[1], row[2], row[3])
        for i in range(4, len(row)):
            if row[i] == "":
                continue  # don't add blank cells
            new_election.add_result(csv_data[0][i], int(row[i]))
        elections.append(new_election)
    return elections


def load_data_folder(folder_path):
    """
    Loads all files in a folder, parsing any csv files and returning a list of Election objects for all the csv
    files in the folder. This function expects the files to be in a specific format, see the accompanying CSV files
    for examples.

    :param folder_path: Folder to convert files from.
    :return: list: List of Election objects containing election data from all the files in folder_path
    """
    elections = []
    for file_path in get_files_in_folder(folder_path):
        if file_path.endswith(".csv"):
            elections += load_data_file(file_path)
    return elections


def state_code_list():
    return ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
            "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
            "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


def write_state_year_csv(a_percentages, a_file_path, a_separator_lines=2):
    with open(a_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for state_code in a_percentages.keys():
            csvwriter.writerow([state_code])
            csvwriter.writerow(["Year"] + list(a_percentages[state_code].keys()))
            csvwriter.writerow(["Democrat"] + [result["Democrat"] for result in a_percentages[state_code].values()])
            csvwriter.writerow(["Republican"] + [result["Republican"] for result in a_percentages[state_code].values()])
            csvwriter.writerow(["Other"] + [result["Other"] for result in a_percentages[state_code].values()])
            for line in range(a_separator_lines):
                csvwriter.writerow([" "])


def write_year_csv(a_percentages, a_file_path):
    with open(a_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Totals"])
        csvwriter.writerow(["Year"] + list(a_percentages.keys()))
        csvwriter.writerow(["Democrat"] + [result["Democrat"] for result in a_percentages.values()])
        csvwriter.writerow(["Republican"] + [result["Republican"] for result in a_percentages.values()])
        csvwriter.writerow(["Other"] + [result["Other"] for result in a_percentages.values()])
