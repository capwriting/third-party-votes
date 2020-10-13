# Developed and tested in Python 3.8.6-amd64 on Windows
from data_tools import tools

def main():
    """
    Loads the csv data in election_data_folder and looks for unique party names across
    all of the election files. Outputs a list of all the unique names and saves it to
    party_name_output_file.

    :return:
    """
    election_data_folder = "..\\data\\hor"
    party_name_output_file  = "..\\party_lists\\unique_parties.txt"

    elections = tools.load_data_folder(election_data_folder)
    unique_parties = []
    for election in elections:
        for party_name in election.results():
            if party_name not in unique_parties:
                unique_parties.append(party_name)

    unique_parties = sorted(unique_parties)
    tools.write_list_to_file(unique_parties, party_name_output_file)


if __name__ == "__main__":
    main()