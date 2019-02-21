#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : etc.py
# Create date : 2019-01-30 15:17
# Modified date : 2019-02-21 20:23
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import string
import torch

config = {}
#base
config["epoch_only"] = True
config["early_stop_epoch"] = True
config["early_stop_epoch_limit"] = 5
config["early_stop_step"] = True
config["early_stop_step_limit"] = 100

config["train_load_check_point_file"] = True
config["batch_size"] = 1000
config["print_every"] = 5
config["num_workers"] = 4
config["max_epoch_stop"] = True
config["epochs"] = 100
config["max_step_stop"] = True
config["steps"] = 100000
#config["device"] = torch.device("cuda" if torch.cuda.is_available() else "cpu")
config["device"] = torch.device("cpu")

config["loss"] = "NLL"
config["optimizer"] = "SGD"
#config["optimizer"] = "momentum"
#base

config["dataset"] = "names"
#config["data_path"] = "./data"
config["data_path"] = "./data/%s" % config["dataset"]
config["learn_rate"] = 0.0005 # If you set this too high, it might explode. If too low, it might not learn
config["momentum"] = 0.9
config["all_letters"] = all_letters = string.ascii_letters + " .,;'-"
config["n_letters"] = len(config["all_letters"]) + 1

config["n_hidden"] = 128
config["train_epoch_steps"] = 10
config["eval_epoch_steps"] = 10
