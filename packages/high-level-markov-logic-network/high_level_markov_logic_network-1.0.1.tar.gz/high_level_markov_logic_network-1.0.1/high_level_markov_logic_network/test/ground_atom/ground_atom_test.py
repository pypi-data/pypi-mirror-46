from high_level_markov_logic_network.ground_atom import GroundAtom

TEST_GROUND_ATOM_1 = 'test(test1)'
TEST_GROUND_ATOM_2 = 'test(test1,test2)'

one_instance_ground_atom_1 = GroundAtom('test', ['test1'])
one_instance_ground_atom_2 = GroundAtom('test', ['test2'])
one_instance_ground_atom_3 = GroundAtom('test', ['test1'], 0.0)

two_instances_ground_atom_1 = GroundAtom('test', ['test1', 'test2'])
two_instances_ground_atom_2 = GroundAtom('test', ['test1', 'test2'])


def test_should_return_str_representation_of_one_instance_ground_atom():
    assert str(one_instance_ground_atom_1) == TEST_GROUND_ATOM_1


def test_should_return_str_representation_of_two_instances_ground_atom():
    assert str(two_instances_ground_atom_1) == TEST_GROUND_ATOM_2


def test_should_return_true_if_ground_atoms_represents_the_same_fact():
    assert two_instances_ground_atom_1 == two_instances_ground_atom_2


def test_should_return_false_if_ground_atoms_have_different_truth_value():
    assert not one_instance_ground_atom_1 == one_instance_ground_atom_3


def test_should_return_false_if_ground_atoms_have_different_instance_values():
    assert not one_instance_ground_atom_1 == one_instance_ground_atom_2


def test_should_return_false_if_ground_atoms_have_different_instance_number():
    assert not one_instance_ground_atom_1 == two_instances_ground_atom_1
