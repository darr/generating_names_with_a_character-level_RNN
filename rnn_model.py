#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : rnn_model.py
# Create date : 2019-02-19 19:43
# Modified date : 2019-02-21 20:26
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import torch
import torch.nn as nn

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, n_categories):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size

        self.input_to_hidden = nn.Linear(n_categories + input_size + hidden_size, hidden_size)
        self.input_to_output = nn.Linear(n_categories + input_size + hidden_size, output_size)
        self.output_to_output = nn.Linear(hidden_size + output_size, output_size)
        self.dropout = nn.Dropout(0.1)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, category, input, hidden):
        input_combined = torch.cat((category, input, hidden), 1)
        hidden = self.input_to_hidden(input_combined)
        output = self.input_to_output(input_combined)
        output_combined = torch.cat((hidden, output), 1)
        output = self.output_to_output(output_combined)
        output = self.dropout(output)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.hidden_size)
