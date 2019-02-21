#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : name_dataset.py
# Create date : 2019-02-16 15:11
# Modified date : 2019-02-20 21:54
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import open
import glob
import unicodedata
import os
import random

import torch
import rnn_model

def _find_files(path):
    return glob.glob(path)

def _unicode_to_ascii(s, config):
    all_letters = config["all_letters"]
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in all_letters
    )

def _read_lines(filename, config):
    lines = open(filename, encoding='utf-8').read().strip().split('\n')
    return [_unicode_to_ascii(line, config) for line in lines]

def _get_all_categories(config):
    category_lines = {}
    all_categories = []

    for filename in _find_files('data/names/*.txt'):
        category = os.path.splitext(os.path.basename(filename))[0]
        all_categories.append(category)
        lines = _read_lines(filename, config)
        category_lines[category] = lines

    return category_lines, all_categories

def _letter_to_index(letter, config):
    all_letters = config["all_letters"]
    return all_letters.find(letter)

def _letter_to_tensor(letter, config):
    n_letters = config["n_letters"]
    tensor = torch.zeros(1, n_letters)
    tensor[0][_letter_to_index(letter, config)] = 1
    return tensor

def _line_to_tensor(line, config):
    n_letters = config["n_letters"]
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][_letter_to_index(letter, config)] = 1
    return tensor

def _random_choice(l):
    return l[random.randint(0, len(l) - 1)]

def random_training_pair(data_dict):
    category_lines = data_dict["category_lines"]
    all_categories = data_dict["all_categories"]
    #print("all_categories:%s" % all_categories)
    category = _random_choice(all_categories)
    #print("category:%s" % category)
    line = _random_choice(category_lines[category])
    #print("line:%s" % line)
    return category, line

def category_from_output(output, all_categories):
    top_n, top_i = output.topk(1)
    category_i = top_i[0].item()
    return all_categories[category_i], category_i


def get_data_dict(config):
    category_lines, all_categories = _get_all_categories(config)
    data_dict = {}
    data_dict["category_lines"] = category_lines
    data_dict["all_categories"] = all_categories
    data_dict["n_categories"] = len(all_categories)
    return data_dict

def line_to_tensor(line, config):
    return _line_to_tensor(line, config)

def _dataset_test(rnn, all_categories, config):
    n_hidden = config["n_hidden"]
    input = _letter_to_tensor('A', config)
    hidden = torch.zeros(1, n_hidden)
    output, next_hidden = rnn(input, hidden)
    input = _line_to_tensor('Albert', config)
    hidden = torch.zeros(1, n_hidden)
    output, next_hidden = rnn(input[0], hidden)
    print(output)
    print(category_from_output(output, all_categories))
    return output

#   def _random_train_example_test(all_categories, category_lines, config):
#       for i in range(10):
#           category, line, category_tensor, line_tensor = random_training_example(all_categories, category_lines, config)
#           print('category =', category, '/ line =', line)

def _test_turn_tensor(config):
    print(_letter_to_tensor('J', config))
    print(_line_to_tensor('Jones', config).size())

def do_test(config):
    _test_turn_tensor(config)
    data_dict = get_data_dict(config)
    category_lines = data_dict["category_lines"]
    all_categories = data_dict["all_categories"]
    n_categories = data_dict["n_categories"]
#    _random_train_example_test(all_categories, category_lines, config)

    n_letters = config["n_letters"]
    n_categories = data_dict["n_categories"]
    n_hidden = config["n_hidden"]
    rnn = rnn_model.RNN(n_letters, n_hidden, n_categories)
    print(_dataset_test(rnn, all_categories, config))

######################################################################
# For each timestep (that is, for each letter in a training word) the
# inputs of the network will be
# ``(category, current letter, hidden state)`` and the outputs will be
# ``(next letter, next hidden state)``. So for each training set, we'll
# need the category, a set of input letters, and a set of output/target
# letters.
#
# Since we are predicting the next letter from the current letter for each
# timestep, the letter pairs are groups of consecutive letters from the
# line - e.g. for ``"ABCD<EOS>"`` we would create ("A", "B"), ("B", "C"),
# ("C", "D"), ("D", "EOS").
#
# .. figure:: https://i.imgur.com/JH58tXY.png
#    :alt:
#
# The category tensor is a `one-hot
# tensor <https://en.wikipedia.org/wiki/One-hot>`__ of size
# ``<1 x n_categories>``. When training we feed it to the network at every
# timestep - this is a design choice, it could have been included as part
# of initial hidden state or some other strategy.
#

# One-hot vector for category
def get_category_tensor(category, data_dict):
    all_categories = data_dict["all_categories"]
    n_categories = data_dict["n_categories"]
    li = all_categories.index(category)
    tensor = torch.zeros(1, n_categories)
    tensor[0][li] = 1
    return tensor

# One-hot matrix of first to last letters (not including EOS) for input
def get_input_tensor(line, config):
    all_letters = config["all_letters"]
    n_letters = config["n_letters"]
    tensor = torch.zeros(len(line), 1, n_letters)
    for li in range(len(line)):
        letter = line[li]
        tensor[li][0][all_letters.find(letter)] = 1
    return tensor

# LongTensor of second letter to end (EOS) for target
def get_target_tensor(line, config):
#   print("line:%s" % line)
    all_letters = config["all_letters"]
#    print("all_letters:%s" % all_letters)
    n_letters = config["n_letters"]
#   print("n_letters:%s" % n_letters)
    letter_indexes = [all_letters.find(line[li]) for li in range(1, len(line))]
#   print("letter_indexes:%s" % letter_indexes)
    letter_indexes.append(n_letters - 1) # EOS
    return torch.LongTensor(letter_indexes)

# Make category, input, and target tensors from a random category, line pair
def random_training_example(data_dict, config):
    category, line = random_training_pair(data_dict)
    category_tensor = get_category_tensor(category, data_dict)
    input_line_tensor = get_input_tensor(line, config)
    target_line_tensor = get_target_tensor(line, config)
#   print("category_tensor")
#   print(category_tensor)
#   print("input_line_tensor")
#   print(input_line_tensor)
#   print("target_line_tensor")
#   print(target_line_tensor)
    return category_tensor, input_line_tensor, target_line_tensor

#   def random_training_example(all_categories, category_lines, config):
#       category = _random_choice(all_categories)
#       line = _random_choice(category_lines[category])
#       category_tensor = torch.tensor([all_categories.index(category)], dtype=torch.long)
#       line_tensor = _line_to_tensor(line, config)
#       return category, line, category_tensor, line_tensor


def get_random_training_input_dict(data_dict, config):
    category_tensor, input_line_tensor, target_line_tensor = random_training_example(data_dict, config)
    model_input_dict = {}
    model_input_dict["category_tensor"] = category_tensor
    model_input_dict["input_line_tensor"] = input_line_tensor
    model_input_dict["target_line_tensor"] = target_line_tensor
    return model_input_dict
