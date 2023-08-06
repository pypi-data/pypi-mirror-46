class GroundAtom():
    def __init__(self, predicate, instances, truth_value=1.0):
        self.predicate = predicate
        self.instances = instances
        self.truth_value = truth_value

    def __str__(self):
        instances_formatted = ','.join(self.instances)
        return '{}({})'.format(self.predicate, instances_formatted)

    def __eq__(self, other):
        if self.predicate == other.predicate and \
                self.instances == other.instances and \
                self.truth_value == other.truth_value:

            return True
        else:
            return False
