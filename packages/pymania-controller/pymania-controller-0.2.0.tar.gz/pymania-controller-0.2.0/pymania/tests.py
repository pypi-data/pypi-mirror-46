import collections
import unittest

from pymania.__main__ import topological_plugin_sort
from pymania.plugins import gui, chat

Plugin = collections.namedtuple('Plugin', ['name', 'depends'])
Widget = collections.namedtuple('Widget', ['size', 'absolute_pos'], defaults=[None, None])

class PluginTest(unittest.TestCase):
    def missing_deps(self):
        list(topological_plugin_sort({
            'a': Plugin('a', {'b', 'c'}),
            'b': Plugin('b', {'d'}),
            'c': Plugin('c', {}),
        }))

    def circular_deps(self):
        list(topological_plugin_sort({
            'a': Plugin('a', {'b'}),
            'b': Plugin('b', {'a'}),
        }))

    def test_sorting(self):
        with self.assertRaises(ImportError):
            self.missing_deps()
        with self.assertRaises(RecursionError):
            self.circular_deps()
        self.assertListEqual(list(topological_plugin_sort({
            'a': Plugin('a', {'b', 'c'}),
            'b': Plugin('b', {'c'}),
            'c': Plugin('c', {}),
            'd': Plugin('d', {}),
        })), [
            {'c', 'd'},
            {'b'},
            {'a'},
        ])

class ChatCommandTest(unittest.TestCase):
    def setUp(self):
        self.parser = chat.CommandParser('cmd')
        self.parser.add_argument('--test')
        subparsers = self.parser.add_subparsers()
        subcommand = subparsers.add_parser('subcommand')
        subcommand.add_argument('--some-option', action='store_true')

    def test_error(self):
        with self.assertRaises(chat._CommandError):
            self.parser.parse_args(['--invalid-option'])
    
    def test_help(self):
        with self.assertRaises(chat._HelpError):
            print(self.parser.parse_args(['subcommand']))
            self.parser.parse_args(['subcommand', '--help'])

class GuiTest(unittest.TestCase):
    def invalid_layout(self):
        list(gui._get_layout(
            padding=gui.Padding(10, 10, 10, 10),
            spacing=gui.Spacing(0, 0),
            items=[Widget(gui.Size(100, 100))]
        ))

    def test_layout(self):
        with self.assertRaises(gui.InvalidLayout):
            self.invalid_layout()
        self.assertListEqual(list(gui._get_layout(
            padding=gui.Padding(10, 10, 0, 10),
            spacing=gui.Spacing(10, 0),
            items=[
                Widget(gui.Size(40, 10)),
                Widget(gui.Size(30, 8)),
                Widget(gui.Size(30, 10)),
                Widget(gui.Size(20, 30)),
                Widget(gui.Size(50, 20)),
            ]
        )), [
            (Widget(gui.Size(40, 10)), gui.Point(10, 10)),
            (Widget(gui.Size(30, 8)), gui.Point(50, 10)),
            (Widget(gui.Size(30, 10)), gui.Point(10, 30)),
            (Widget(gui.Size(20, 30)), gui.Point(40, 30)),
            (Widget(gui.Size(50, 20)), gui.Point(10, 70)),
        ])

if __name__ == '__main__':
    unittest.main()
