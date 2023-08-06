from high_level_markov_logic_network.ground_atom import GroundAtom
from word_net import determine_path_similarity_between_two_concepts

__IS_A__ = 'is_a'


def get_is_a_ground_atoms(a, concepts):
    is_a_ground_atoms = []

    for concept in concepts:
        is_a_ground_atoms.append(get_is_a_ground_atom(a, concept))

    return is_a_ground_atoms


def get_is_a_ground_atom(a, b):
    similarity = determine_path_similarity_between_two_concepts(a, b)

    return GroundAtom(__IS_A__, [a, b], similarity)