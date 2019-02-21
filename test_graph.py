#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : test_graph.py
# Create date : 2019-02-19 21:24
# Modified date : 2019-02-21 20:27
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import name_dataset
import torch

from graph import RNNGraph
import record

def _normalize_confusion(n_categories, confusion):
    for i in range(n_categories):
        confusion[i] = confusion[i] / confusion[i].sum()
    return confusion

class TestRNNGraph(RNNGraph):
    def __init__(self, data_dict, config):
        super(TestRNNGraph, self).__init__(data_dict, config)
        self._load_train_model("test")

    def _test_a_epoch(self):
        self.samples('Russian', 'RUS')
        self.samples('Russian', 'RUS')
        self.samples('German', 'GER')
        self.samples('Spanish', 'SPA')
        self.samples('Chinese', 'CHI')

    def _init_best_step_model(self):
        record.save_content(self.config, "best step model")
        model = self.graph_dict["model"]
        model.load_state_dict(self.status_dict["best_step_model_wts"])

    def _init_best_epoch_model(self):
        record.save_content(self.config, "best epoch model")
        model = self.graph_dict["model"]
        model.load_state_dict(self.status_dict["best_epoch_model_wts"])

    def _test_best_step_model(self):
        self._init_best_step_model()
        self._test_a_epoch()

    def _test_best_epoch_model(self):
        self._init_best_epoch_model()
        self._test_a_epoch()

    def test_the_model(self):
        self._test_best_step_model()
        self._test_best_epoch_model()

    def sample(self, category, start_letter='A'):
        rnn = self.graph_dict["model"]
        data_dict = self.data_dict
        config = self.config
        n_letters = config["n_letters"]
        all_letters = config["all_letters"]
        max_length = 20
        with torch.no_grad():
            category_tensor = name_dataset.get_category_tensor(category, data_dict)
            ipt = name_dataset.get_input_tensor(start_letter, config)
            hidden = rnn.init_hidden()
            output_name = start_letter
            for i in range(max_length):
                output, hidden = rnn(category_tensor, ipt[0], hidden)
                topv, topi = output.topk(1)
                topi = topi[0][0]
                if topi == n_letters - 1:
                    break
                else:
                    letter = all_letters[topi]
                    output_name += letter
                ipt = name_dataset.get_input_tensor(letter, config)
            return output_name

    def samples(self, category, start_letters='ABC'):
        for start_letter in start_letters:
            record.save_content(self.config, "%s start:%s" % (category, start_letter))
            con = self.sample(category, start_letter)
            record.save_content(self.config, con)
