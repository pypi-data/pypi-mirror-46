from os.path import join, abspath,dirname

from pracmln import PRACMLNConfig, MLN
from pracmln.utils.project import MLNProject

from high_level_markov_logic_network.markov_logic_network import MarkovLogicNetwork

TEST_FILE_PATH = abspath(__file__)
ROOT_PATH = dirname(TEST_FILE_PATH)
TEST_MLN_PATH = join(ROOT_PATH, 'test.pracmln')


def test_should_init_a_successful_markov_logic_network_object():
    mln = MarkovLogicNetwork(TEST_MLN_PATH)

    assert mln.__grammar__ == 'PRACGrammar'
    assert isinstance(mln.__config__, PRACMLNConfig)
    assert isinstance(mln.domains, dict)
    assert isinstance(mln.pracmln, MLN)
    assert isinstance(mln.pracmln_project, MLNProject)
    assert mln.__logic__ == 'FuzzyLogic'
    assert mln.__mln_name__ == 'grasping_type.mln'