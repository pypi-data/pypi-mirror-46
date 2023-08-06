import pytest
from unittest.mock import patch

from ..actions import AppendIdValuePair
from ..parser import YoctolArgumentParser


@pytest.fixture(scope='module')
def yoctol_parser():
    parser = YoctolArgumentParser(prog='main.py')
    parser.add_argument(
        '--foo',
        action=AppendIdValuePair,
        id_choices=['a', 'b'],
        value_metavar='boo',
        value_type=int,
    )
    return parser


def test_append(yoctol_parser):
    with patch('sys.argv', 'main.py --foo a 1 --foo b 2 --foo a 3'.split(' ')):
        args = yoctol_parser.parse_args()
    assert args.foo == [('a', 1), ('b', 2), ('a', 3)]


@pytest.mark.parametrize('invalid_arg', [
    pytest.param('main.py --foo a', id='invalid_nargs'),
    pytest.param('main.py --foo a 1 b', id='invalid_nargs'),
    pytest.param('main.py --foo c 1', id='invalid_choice'),
    pytest.param('main.py --foo a b', id='invalid_value'),
])
def test_raise_invalid_arg(yoctol_parser, invalid_arg):
    argv = invalid_arg.split()
    with patch('sys.argv', argv), pytest.raises(SystemExit) as exc_info:
        yoctol_parser.parse_args()
    assert exc_info.value.code == 2
