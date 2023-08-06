#!/usr/bin/env python3
# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from argparse import ArgumentParser
from fitipy import Fitipy
from keras.callbacks import LambdaCallback
from os.path import splitext, isfile
from prettyparse import add_to_parser, create_parser
from typing import Any, Tuple

from precise.model import create_model, ModelParams
from precise.params import inject_params, save_params
from precise.train_data import TrainData
from precise.util import calc_sample_hash

usage = '''
    Package a dataset into a numpy file

    :output_file str
        Numpy npz file to write dataset to
    
    :-p --params-file str -
        Params file to read from

    ...
'''


def main():
    parser = create_parser(usage)
    args = TrainData.parse_args(parser)
    if args.params_file:
        inject_params(args.params_file.replace('.params', ''))
    data = TrainData.from_both(args.tags_file, args.tags_folder, args.folder)
    (train_in, train_out), (test_in, test_out) = data.load()
    import numpy as np
    np.save


if __name__ == '__main__':
    main()
