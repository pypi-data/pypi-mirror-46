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
        "\.container",
        "\.git",
        "\.hg",
        "\.mypy_cache",
        "\.nox",
        "\.om",
        "\.tox",
        "\.venv",
        "__manifest__.py",
        "_build",
        "_lib",
        "_lib_static",
        "dist",
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
        cmd = "black {options} {source}".format(
            options=self._get_black_options(), source=self.options.get("--source", False) or "."
        )

        if self.options.get("--verbose", False):
            shell.out(cmd)

        shell.run(cmd)

    def _get_black_options(self):
        """
        Format a set of options to pass to black.

        :return {str}: Formatted set of cli options for black.
        """
        return "-l {line_length} --exclude '{excludes}'".format(
            line_length=self.line_length,
            excludes="(__manifest__.py|__openerp__.py|/({})/)".format("|".join(self.excludes)),
        )
