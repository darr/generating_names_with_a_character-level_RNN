#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : main.py
# Create date : 2019-02-01 17:22
# Modified date : 2019-02-20 21:41
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

#from io import open
#import glob
#import os
#import unicodedata
#import string
#import random
#import time
#import math

#import torch
#import torch.nn as nn
#import torch.optim as optim

from etc import config
#from rnn_model import RNN
import name_dataset
#import status
import test_graph
import train_graph

data_dict = name_dataset.get_data_dict(config)
train_g = train_graph.TrainRNNGraph(data_dict, config)
train_g.train_the_model()

test_g = test_graph.TestRNNGraph(data_dict, config)
test_g.test_the_model()
