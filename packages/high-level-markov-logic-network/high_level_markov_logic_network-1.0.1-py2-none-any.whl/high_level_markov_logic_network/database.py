from pracmln.mln.database import Database as PRACMLNDatabase


class Database:
    def __init__(self, mln):
        self.pracmln_database = PRACMLNDatabase(mln.pracmln)
        self.ground_atoms = []

    def add_ground_atom(self, ground_atom):
        self.ground_atoms.append(ground_atom)
        self.pracmln_database.add(str(ground_atom), ground_atom.truth_value)