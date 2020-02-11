class State:
    def __init__(self, set_message):
        self._nb_rows = set_message[0]
        self._nb_columns = set_message[1]

    @property
    def nb_rows(self):
        return self._nb_rows

    @property
    def nb_columns(self):
        return self._nb_columns



