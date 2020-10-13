# Developed and tested in Python 3.8.6-amd64 on Windows
from data_tools import tools


class PartyNotFound(Exception):
    pass


class InvalidStateCode(Exception):
    pass

def get_totals(a_elections, a_race_qualifiers=None):
    vote_tallies = {}
    party_classifications = {"Democrat": tools.read_list_from_file("..\\party_lists\\dem.txt"),
                             "Republican": tools.read_list_from_file("..\\party_lists\\rep.txt"),
                             "Other": tools.read_list_from_file("..\\party_lists\\other.txt")}

    for election in a_elections:
        if (a_race_qualifiers is not None) and (election.race not in a_race_qualifiers):
            continue  # Skip any elections which don't meet race qualifiers
        if election.state not in tools.state_code_list():
            raise InvalidStateCode("{state} is not a valid state code!".format(state=election.state))
        if election.year not in vote_tallies.keys():
            vote_tallies[election.year] = {"Democrat": 0,
                                           "Republican": 0,
                                           "Other": 0}
        # Add vote tallies to the correct state and year
        for party_name, vote_tally in election.results().items():
            if party_name in party_classifications["Democrat"]:
                vote_tallies[election.year]["Democrat"] += vote_tally
            elif party_name in party_classifications["Republican"]:
                vote_tallies[election.year]["Republican"] += vote_tally
            elif party_name in party_classifications["Other"]:
                vote_tallies[election.year]["Other"] += vote_tally
            else:
                raise PartyNotFound(
                    "{party_name} does not appear in party classifications.".format(party_name=party_name))

    return vote_tallies


def calculate_percent(a_elections, a_race_qualifiers=None):
    total_percents = {}
    vote_tallies = get_totals(a_elections, a_race_qualifiers)

    # Calculate percentages
    for year in vote_tallies.keys():
        vote_total = sum(vote_tallies[year].values())

        total_percents[year] = {"Democrat": (vote_tallies[year]["Democrat"] / vote_total) * 100,
                                "Republican": (vote_tallies[year]["Republican"] / vote_total) * 100,
                                "Other": (vote_tallies[year]["Other"] / vote_total) * 100}

    return total_percents

def get_totals_by_state(a_elections, a_race_qualifiers=None):
    state_vote_tallies = {}
    party_classifications = {"Democrat": tools.read_list_from_file("..\\party_lists\\dem.txt"),
                             "Republican": tools.read_list_from_file("..\\party_lists\\rep.txt"),
                             "Other": tools.read_list_from_file("..\\party_lists\\other.txt")}

    for election in a_elections:
        if (a_race_qualifiers is not None) and (election.race not in a_race_qualifiers):
            continue  # Skip any elections which don't meet race qualifiers
        if election.state not in tools.state_code_list():
            raise InvalidStateCode("{state} is not a valid state code!".format(state=election.state))
        # Add dictionary elements if they DNE
        if election.state not in state_vote_tallies.keys():
            state_vote_tallies[election.state] = {}
        if election.year not in state_vote_tallies[election.state].keys():
            state_vote_tallies[election.state][election.year] = {"Democrat": 0,
                                                                 "Republican": 0,
                                                                 "Other": 0}
        # Add vote tallies to the correct state and year
        for party_name, vote_tally in election.results().items():
            if party_name in party_classifications["Democrat"]:
                state_vote_tallies[election.state][election.year]["Democrat"] += vote_tally
            elif party_name in party_classifications["Republican"]:
                state_vote_tallies[election.state][election.year]["Republican"] += vote_tally
            elif party_name in party_classifications["Other"]:
                state_vote_tallies[election.state][election.year]["Other"] += vote_tally
            else:
                raise PartyNotFound(
                    "{party_name} does not appear in party classifications.".format(party_name=party_name))

    return state_vote_tallies


def calculate_percent_by_state(a_elections, a_race_qualifiers=None):
    total_percents = {}
    state_vote_tallies = get_totals_by_state(a_elections, a_race_qualifiers)

    # Calculate percentages
    for state_code in state_vote_tallies:
        total_percents[state_code] = {}
        for year in state_vote_tallies[state_code].keys():
            state_vote_total = sum(state_vote_tallies[state_code][year].values())

            total_percents[state_code][year] = {"Democrat": (state_vote_tallies[state_code][year]["Democrat"] / state_vote_total) * 100,
                                          "Republican": (state_vote_tallies[state_code][year][
                                                             "Republican"] / state_vote_total) * 100,
                                          "Other": (state_vote_tallies[state_code][year]["Other"] / state_vote_total) * 100}

    return total_percents


def main():
    election_data_folder = "..\\data\\hor"
    elections = tools.load_data_folder(election_data_folder)

    total_tallies_state = get_totals_by_state(elections)
    president_tallies_state = get_totals_by_state(elections, a_race_qualifiers=["President"])
    senate_tallies_state = get_totals_by_state(elections, a_race_qualifiers=["Senator"])
    hor_tallies_state = get_totals_by_state(elections, a_race_qualifiers=["Representative", "Delegate"])

    total_percentages_state = calculate_percent_by_state(elections)
    president_percentages_state = calculate_percent_by_state(elections, a_race_qualifiers=["President"])
    senate_percentages_state = calculate_percent_by_state(elections, a_race_qualifiers=["Senator"])
    hor_percentages_state = calculate_percent_by_state(elections, a_race_qualifiers=["Representative", "Delegate"])

    total_percentages = calculate_percent(elections)
    president_percentages = calculate_percent(elections, a_race_qualifiers=["President"])
    senate_percentages = calculate_percent(elections, a_race_qualifiers=["Senator"])
    hor_percentages = calculate_percent(elections, a_race_qualifiers=["Representative"])

    csv_separator_lines = 2  # This is to provide ample space between entries when copy/pasting into Google Sheets

    tools.write_state_year_csv(total_tallies_state, "..\\total_tallies_state.csv", csv_separator_lines)
    tools.write_state_year_csv(president_tallies_state, "..\\president_tallies_state.csv", csv_separator_lines)
    tools.write_state_year_csv(senate_tallies_state, "..\\senate_tallies_state.csv", csv_separator_lines)
    tools.write_state_year_csv(hor_tallies_state, "..\\hor_tallies_state.csv", csv_separator_lines)

    tools.write_state_year_csv(total_percentages_state, "..\\total_percentages_state.csv", csv_separator_lines)
    tools.write_state_year_csv(president_percentages_state, "..\\president_percentages_state.csv", csv_separator_lines)
    tools.write_state_year_csv(senate_percentages_state, "..\\senate_percentages_state.csv", csv_separator_lines)
    tools.write_state_year_csv(hor_percentages_state, "..\\hor_percentages_state.csv", csv_separator_lines)

    tools.write_year_csv(total_percentages, "..\\total_percentages.csv")
    tools.write_year_csv(president_percentages, "..\\president_percentages.csv")
    tools.write_year_csv(senate_percentages, "..\\senate_percentages.csv")
    tools.write_year_csv(hor_percentages, "..\\hor_percentages.csv")


if __name__ == "__main__":
    main()
