class Election:
    def __init__(self, a_year, a_state, a_race, a_division):
        if a_year == "" or not a_year.isnumeric():
            raise ValueError("{year} is not a valid year!".format(year = a_year))
        self.year = a_year
        self.state = a_state
        self.race = a_race
        self.division = a_division
        self._results = {}

    def __repr__(self):
        description_string = "{year} {state} {race} Election, Division {division}:\n".format(year = self.year,
                                                                                            state = self.state,
                                                                                            race = self.race,
                                                                                            division = self.division)
        if len(self._results) <= 0:
            description_string += "\tNo results.\n"
        else:
            for party_name, vote_tally in self._results.items():
                description_string += "\t{party_name}: {vote_tally}\n".format(party_name = party_name,
                                                                              vote_tally = vote_tally)
            description_string += "\tTotal: {total_votes}\n".format(total_votes = self.total_votes())
        return description_string

    def __str__(self):
        return self.__repr__()

    def add_result(self, a_party_name, a_vote_tally):
        if not isinstance(a_vote_tally, int):
            raise ValueError("Vote tally must be an integer. {value} is not an integer!".format(value=a_vote_tally))
        if a_party_name not in self._results.keys():
            self._results[a_party_name] = a_vote_tally
        else:
            raise DuplicatePartyName("{party_name} already has a record in this election!".format(party_name = a_party_name))

    def total_votes(self):
        return sum(self._results.values())

    def vote_percentages(self):
        return {party_name: (vote_tally / self.total_votes()) for party_name, vote_tally in self._results.items()}

    def results(self):
        return self._results


class DuplicatePartyName(Exception):
    pass
