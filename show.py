#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : show.py
# Create date : 2019-02-11 14:37
# Modified date : 2019-02-18 17:43
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import record

def _get_list(category_name, key_name, list_name, status_dict):
    l = status_dict[list_name]
    x = []
    y = []
    for dic in l:
        y_value = dic[key_name]
        y.append(y_value)
        x_value = dic[category_name]
        x.append(x_value)
    return y, x

def _show_list(category_name, data_key, status_dict, config):
    name = "%s_%s.jpg" % (category_name, data_key)
    train_list_name = "train_%s_%s" % (category_name, data_key)
    eval_list_name = "eval_%s_%s" % (category_name, data_key)

    train_lt, train_step = _get_list(category_name, data_key, "%s_list" % train_list_name, status_dict)
    eval_lt, eval_step = _get_list(category_name, data_key, "%s_list" % eval_list_name, status_dict)

    l1, = plt.plot(train_step, train_lt)
    l2, = plt.plot(eval_step, eval_lt)

    line_lt = [l1, l2]
    labels_lt = (train_list_name, eval_list_name)
    _write_jpg(line_lt, labels_lt, name, config)

def _write_jpg(line_lt, labels_lt, name, config):
    plt.legend(handles=line_lt, labels=labels_lt, loc='best')
    save_path = record.get_check_point_path(config)
    full_path_name = "%s/%s" % (save_path, name)
    plt.savefig(full_path_name)
    plt.close()

def show_epoch_loss(status_dict, config):
    category_name = "epoch"
    data_key = "loss"
    _show_list(category_name, data_key, status_dict, config)

def show_step_loss(status_dict, config):
    category_name = "step"
    data_key = "loss"
    _show_list(category_name, data_key, status_dict, config)

def show_epoch_acc(status_dict, config):
    category_name = "epoch"
    data_key = "acc"
    _show_list(category_name, data_key, status_dict, config)

def show_step_acc(status_dict, config):
    category_name = "step"
    data_key = "acc"
    _show_list(category_name, data_key, status_dict, config)

def show_confusion(confusion, data_dict, config):
    all_categories = data_dict["all_categories"]
    # Set up plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(confusion.numpy())
    fig.colorbar(cax)

    # Set up axes
    ax.set_xticklabels([''] + all_categories, rotation=90)
    ax.set_yticklabels([''] + all_categories)

    # Force label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    # sphinx_gallery_thumbnail_number = 2
    name = "confusion"
    save_path = record.get_check_point_path(config)
    full_path_name = "%s/%s" % (save_path, name)
    plt.savefig(full_path_name)
    plt.close()
