from high_level_markov_logic_network.fuzzy_markov_logic_network.is_a_generator import get_is_a_ground_atoms

A = 'cup.n.01'
CONCEPTS = ['cup.n.01', 'can.n.01']

PATH_SIM_BETWEEN_CUP_CAN = 0.33
PATH_SIM_BETWEEN_CUP_CUP = 1.0


def test_should_return_a_valid_list_of_is_a_ground_atoms():
    is_a_ground_atoms = get_is_a_ground_atoms(A, CONCEPTS)

    is_a_ground_atom = is_a_ground_atoms[0]
    assert str(is_a_ground_atom) == 'is_a(cup.n.01,cup.n.01)'
    assert is_a_ground_atom.truth_value == PATH_SIM_BETWEEN_CUP_CUP

    is_a_ground_atom = is_a_ground_atoms[1]
    assert str(is_a_ground_atom) == 'is_a(cup.n.01,can.n.01)'
    assert round(is_a_ground_atom.truth_value, 2) == PATH_SIM_BETWEEN_CUP_CAN
