import argparse

from .formatters import YoctolFormatter


class YoctolArgumentParser(argparse.ArgumentParser):

    def __init__(
            self,
            prog=None,
            usage=None,
            description=None,
            epilog=None,
            parents=(),
            formatter_class=YoctolFormatter,
            prefix_chars='-',
            fromfile_prefix_chars=None,
            argument_default=None,
            conflict_handler='error',
            add_help=True,
            allow_abbrev=True,
        ):
        super().__init__(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            parents=parents,
            formatter_class=formatter_class,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help,
            allow_abbrev=allow_abbrev,
        )
