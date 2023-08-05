from .base import BaseCommand
from odoo_manager.core import shell, git

try:
    import black
except:
    print("Make sure that you have black installed before running format.")
    exit(1)


class Format(BaseCommand):
    line_length = 120
    excludes = [
        "\.git",
        "\.hg",
        "\.mypy_cache",
        "\.tox",
        "\.nox",
        "\.venv",
        "_build",
        "dist",
        "\.container",
        "_lib",
        "_lib_static",
        "\.om",
        "tasks",
    ]

    def __init__(self, options, *args, **kwargs):
        """
        Initialize the Black command.
        """
        super(Format, self).__init__(options, depends_on_project=False, *args, **kwargs)
        self.supported_commands = "format"

    def run(self):
        """
        Run the formatter.

        :return {NoneType}:
        """
        cmd = "black {options} .".format(options=self._get_black_options())
        shell.out(cmd)
        shell.run(cmd)

    def _get_black_options(self):
        """
        Format a set of options to pass to black.

        :return {str}: Formatted set of cli options for black.
        """
        return "-l {line_length} --exclude '{excludes}'".format(
            line_length=self.line_length, excludes="/({})/".format("|".join(self.excludes))
        )
