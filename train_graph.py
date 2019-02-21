#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : train_graph.py
# Create date : 2019-02-19 21:59
# Modified date : 2019-02-21 20:27
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import time

import name_dataset
import status

from graph import RNNGraph

class TrainRNNGraph(RNNGraph):
    def __init__(self, data_dict, config):
        super(TrainRNNGraph, self).__init__(data_dict, config)

    def eval_a_epoch(self):
        self._eval_a_epoch()

    def train_a_epoch(self):
        self._train_a_epoch()

    def _run_a_epoch(self, epoch):
        status.update_epoch(epoch, self.status_dict)
        start = time.time()
        self.train_a_epoch()
        self.eval_a_epoch()
        end = time.time()

        status.update_elapsed_time(start, end, self.status_dict)
        status.save_epoch_status(self.status_dict, self.config)
        self._save_trained_model()

    def get_model_output(self, model_input_dict):
        config = self.config
        category_tensor = model_input_dict["category_tensor"]
        input_line_tensor = model_input_dict["input_line_tensor"]
        target_line_tensor = model_input_dict["target_line_tensor"]
        target_line_tensor.unsqueeze_(-1)

        input_line_tensor = input_line_tensor.to(config["device"])
        category_tensor = category_tensor.to(config["device"])
        target_line_tensor = target_line_tensor.to(config["device"])

        model = self.graph_dict["model"]
        criterion = self.graph_dict["criterion"]
        loss = 0
        hidden = model.init_hidden()
        hidden = hidden.to(self.config["device"])
        for i in range(input_line_tensor.size(0)):
            input_tensor = input_line_tensor[i]
            output, hidden = model(category_tensor, input_tensor, hidden)
            target_tensor = target_line_tensor[i]
            l = criterion(output, target_tensor)
            loss += l
        return output, loss

    def _deal_a_step(self, model_input_dict, mode="test"):
        criterion = self.graph_dict["criterion"]
        model = self.graph_dict["model"]
        optimizer = self.graph_dict["optimizer"]
        input_line_tensor = model_input_dict["input_line_tensor"]

        if mode == "train":
            model.zero_grad()
            optimizer.zero_grad()

        output, loss = self.get_model_output(model_input_dict)

        if mode == "train":
            loss.backward()
            optimizer.step()

#       return output, loss.item()
        return output, loss.item() / input_line_tensor.size(0)

    def _deal_a_batch(self, step_func):
        data_dict = self.data_dict
        config = self.config
        batch_size = self.config["batch_size"]

        running_loss = 0.0
        running_corrects = 0

        for i in range(0, batch_size):
            model_input_dict = name_dataset.get_random_training_input_dict(data_dict, config)
            output, loss = step_func(model_input_dict)
            running_loss += loss

        avg_acc = running_corrects / batch_size
        avg_loss = running_loss / batch_size
        return avg_loss, avg_acc, running_corrects

    def train_the_model(self):
        self._create_output()
        epoch = self.status_dict["epoch"]

        while True:
            if not self.check_epoch_stop():
                self._run_a_epoch(epoch)
                epoch += 1
            else:
                break

        self.show_the_value()
        return self.graph_dict["model"]
