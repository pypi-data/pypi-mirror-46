import io
import os

from pracmln.mlnquery import MLNQuery
from pracmln.mlnlearn import MLNLearn
from pracmln.utils.project import MLNProject
from pracmln.mln.base import parse_mln
from pracmln.mln.database import parse_db


class MarkovLogicNetwork:
    def __init__(self, path_to_pracmln_project):
        self.__path_to_pracmln_project__ = path_to_pracmln_project
        self.pracmln_project = MLNProject.open(path_to_pracmln_project)
        self.__config__ = self.pracmln_project.queryconf
        self.__logic__ = self.__config__.config['logic']
        self.__grammar__ = self.__config__.config['grammar']
        self.__mln_name__ = self.__config__.config['mln']
        self.pracmln = self.__parse_mln_from_text__()
        self.domains = self.pracmln.domains

    def __parse_mln_from_text__(self):
        mln_text = self.pracmln_project.mlns.get(self.__mln_name__)
        return parse_mln(mln_text, logic=self.__logic__, grammar=self.__grammar__)

    def infer(self, database):
        mln_query = MLNQuery(self.__config__,
                             mln=self.pracmln,
                             db=database.pracmln_database,
                             verbose=0)

        return mln_query.run()

    def learn(self, db_content=None):
        learn_config = self.pracmln_project.learnconf
        logic = learn_config.config['logic']
        grammar = learn_config.config['grammar']
        output_filename = learn_config.config['output_filename']

        train_db_name = learn_config.config['db']

        if not db_content:
            db_content = self.pracmln_project.dbs.get(train_db_name)

        #Load template MLN
        template_mln_name = learn_config.config['mln']
        mln_text = self.pracmln_project.mlns.get(template_mln_name)
        parsed_mln = parse_mln(mln_text, logic=logic, grammar=grammar)

        #Load Database
        db = parse_db(parsed_mln, db_content)

        mln_learn = MLNLearn(learn_config, mln=parsed_mln, db=db)

        learned_mln = mln_learn.run()

        #Read trained MLN as string
        string_out = io.BytesIO()
        learned_mln.write(stream=string_out)
        learned_mln_text = string_out.getvalue()

        self.pracmln_project.add_db(train_db_name, db_content)
        self.pracmln_project.add_mln(output_filename, learned_mln_text)

        #Fixes for project saving after the init of MLNLearn, the learnconfig will be messed up which causes
        #crashes when the project is intended to be saved
        learn_config.config['mln'] = template_mln_name
        learn_config.config['db'] = train_db_name

        self.pracmln_project.save(os.path.dirname(self.__path_to_pracmln_project__))

