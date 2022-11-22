# Copyright 2021 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest

import towhee
from towhee.runtime.runtime_pipeline import Graph
from towhee.runtime.factory import ops, register


#pylint: disable=protected-access
@register
class Add:
    def __init__(self):
        pass

    def __call__(self, x):
        return x + 1


def add(x):
    return x + 1


class TestConfig(unittest.TestCase):
    """
    Unit test for Config.
    """
    def test_map_config(self):
        pipe = towhee.pipe.input('a').map('a', 'b', lambda x: x + 1).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'lambda-0', '_output'])

    def test_flat_map_config(self):
        pipe = towhee.pipe.input('a').flat_map('a', 'b', lambda x: [x + 1]).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'lambda-0', '_output'])

    def test_filter_config(self):
        pipe = towhee.pipe.input('a').filter('a', 'b', 'a', lambda x: True).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'lambda-0', '_output'])

    def test_window_config(self):
        pipe = towhee.pipe.input('a').window('a', 'b', 1, 1, lambda x: x + 1).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'lambda-0', '_output'])

    def test_window_all_config(self):
        pipe = towhee.pipe.input('a').window_all('a', 'b', lambda x: x + 1).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'lambda-0', '_output'])

    def test_time_window_config(self):
        pipe = towhee.pipe.input('a').time_window('a', 'b', 'a', 1, 1, lambda x: x + 1).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'lambda-0', '_output'])

    def test_different_op(self):
        pipe = towhee.pipe.input('a').map('a', 'b', lambda x: x + 1).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'lambda-0', '_output'])
        pipe(1).get()

        pipe = towhee.pipe.input('a').map('a', 'b', add).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'add-0', '_output'])
        pipe(1).get()

        pipe = towhee.pipe.input('a').map('a', 'b', ops.local.add_operator(10)).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'local/add-operator-0', '_output'])
        pipe(1).get()

        pipe = towhee.pipe.input('a').map('a', 'b', ops.Add()).output('a', 'b')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'Add-0', '_output'])
        pipe(1).get()

    def test_multi_lambda(self):
        pipe = towhee.pipe.input('a').map('a', 'b', lambda x: x + 1).map('a', 'c', lambda x: x - 1).output('a', 'b', 'c')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'lambda-0', 'lambda-1', '_output'])

    def test_concat(self):
        pipe0 = towhee.pipe.input('a')
        pipe1 = pipe0.map('a', 'b', lambda x: x + 1)
        pipe2 = pipe0.map('a', 'c', lambda x: x + 2)
        pipe = pipe2.concat(pipe1).output('a', 'b', 'c')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'lambda-0', 'lambda-1', 'concat-2', '_output'])

    def test_same_name(self):
        pipe = towhee.pipe.input('a').map('a', 'b', add).map('b', 'c', add).map('a', 'd', add).output('a', 'b', 'c', 'd')
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'add-0', 'add-1', 'add-2', '_output'])
        self.assertEqual(pipe(1).get(), [1, 2, 3, 2])

    def test_config_user_config(self):
        pipe = (
            towhee.pipe.input('a')
                .map('a', 'b', add, {'name': 'add_1'})
                .map('b', 'c', add, {'name': 'add_1'})
                .map('a', 'd', add, {'name': 'add_2'})
                .output('a', 'b', 'c', 'd')
        )
        graph = Graph(pipe._dag_repr.nodes, pipe._dag_repr.edges, pipe._operator_pool, pipe._thread_pool)
        self.assertEqual([v.name for _, v in graph._nodes.items()], ['_input', 'add_1', 'add_1', 'add_2', '_output'])
        self.assertEqual(pipe(1).get(), [1, 2, 3, 2])
