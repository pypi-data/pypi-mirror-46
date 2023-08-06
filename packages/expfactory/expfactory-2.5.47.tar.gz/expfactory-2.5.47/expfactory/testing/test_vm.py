#!/usr/bin/python

"""
Test experiments
"""

from expfactory.utils import copy_directory, get_installdir
from expfactory.experiment import load_experiment
from expfactory.vm import *
import tempfile
import unittest
import shutil
import json
import os
import re

class TestVm(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.experiment = os.path.abspath("%s/testing/data/test_task/" %self.pwd)
        self.config = json.load(open("%s/testing/data/test_task/config.json" %self.pwd,"rb"))

    def test_database_url(self):
        dburl = generate_database_url(template="mysql")
        self.assertTrue(dburl=="mysql://expfactory:expfactory@localhost:3306/expfactory")

        dburl = generate_database_url(template="sqlite3")
        self.assertTrue(dburl=="sqlite:///participants.db")

        dburl = generate_database_url(template="postgresql")
        self.assertTrue(dburl=="postgresql://expfactory:expfactory@localhost:5432/expfactory")

    def test_jspsych_init(self):

        # Get jspsych init
        init = get_jspsych_init(self.config[0])
        self.assertTrue(re.search("expfactory_finished",init))
        self.assertTrue(re.search("jsPsych.init",init))

        init = get_jspsych_init(self.config[0],deployment="docker-mturk")
        self.assertTrue(re.search("{{next_page}}",init))
        self.assertTrue(re.search("jsPsych.init",init))

        init = get_jspsych_init(self.config[0],deployment="docker-local")
        self.assertTrue(re.search("test_task_experiment",init))
        self.assertTrue(re.search("jsPsych.init",init))

    def test_getstylejs(self):
        experiment = load_experiment(self.experiment)
        stylejs = get_stylejs(experiment)
        self.assertTrue(len(stylejs)==2)
        self.assertTrue(re.search("style.css",stylejs[0])!=None)
        self.assertTrue(re.search("experiment.js",stylejs[1])!=None)

if __name__ == '__main__':
    unittest.main()
