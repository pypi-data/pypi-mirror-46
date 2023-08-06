import os
import sys
from pprint import pprint as pp
from .base import BaseCommand
from odoo_manager.core import shell

try:
    import pypandoc
except:
    print("Make sure that you have pypandoc installed before running convert.", file=sys.stderr)
    exit(1)


class Convert(BaseCommand):
    """
    Using pypandoc, convert a file from one type of formatting to another.

    This can be used to convert from Markdown to HTML and back, as well as many
    other types of supported formats.

    The pypandoc Python package documentation can be found at:
        https://pypi.org/project/pypandoc/

    The pandoc System package documentation can be found at:
        https://pandoc.org/MANUAL.html
    """

    def __init__(self, options, *args, **kwargs):
        """
        Initialize the Convert command.

        :return {NoneType}:
        """
        super(Convert, self).__init__(options, depends_on_project=False, *args, **kwargs)
        self.supported_commands = "convert"

    def run(self):
        """
        Run the conversion tool (pandoc).

        Convert a file from one format into another, such as Markdown to HTML or
        HTML to Markdown.

        Example:
          - odoo_manager convert --source=my_module/readme.md --dest=my_module/static/description/index.html
            - Converts `my_module/readme.md` from Markdown to HTML and
              overwrites the result it to `my_module/static/description/index.html`.

          - odoo_manager convert --source=my_module/readme.md --to=html
            - Converts `my_module/readme.md` from Markdown to HTML and outputs
              the result to shell.

          - odoo_manager convert --source=my_module/readme.md --dest=my_module/static/description/index.html --append
            - Converts `my_module/readme.md` from Markdown to HTML and
              **appends** the result it to `my_module/static/description/index.html`.

        :return {NoneType}:
        """
        paths = self.get_paths()

        if self.options.get("--install", False):
            pypandoc.download_pandoc()

        # Get "From" and "To" file types (if any)
        from_type = self.options.get("--from", False)
        to_type = self.options.get("--to", False)

        # Get Source and Validate its existence
        source = self.options.get("--source", False) or str(input(" > What is the path to the source file? "))
        if not source or not os.path.isfile(paths.base(source)):
            shell.out("The source path ({}) does not appear to exist...".format(source), color="pink", is_error=True)
            exit(1)

        # Get Destination file (if any)
        dest = self.options.get("--dest", False)
        if not dest and not to_type:
            str(input(" > What is the path to the destination file? (Leave blank for output to shell) "))

        # If Destination is provided, then validate it exists
        if dest and not os.path.isfile(paths.base(dest)):
            shell.out("The destination path ({}) does not appear to exist...".format(dest), color="pink", is_error=True)
            exit(1)

        # Destination file or "To" file type must be given for Pandoc to know
        # what to covert the source into.
        if not dest and not to_type:
            shell.out("You must provide a destination path or a file type to convert to", color="pink", is_error=True)
            exit(1)

        # If the type is not provided, then get it from the destination file
        # extension. This is not required for shell command, but it is required
        # for the `convert_file` Python method.
        if not to_type:
            to_type = dest.split(".")[-1]

        append = self.options.get("--append", False)
        verbose = self.options.get("--verbose", False)

        options = self._get_pandoc_python_options(source, dest, from_type, to_type, append)

        try:
            output = pypandoc.convert_file(**options)
        except OSError as error:
            shell.out(
                "Could not run the covert method. Try running convert with the --install flag or see the errors above/below... You can also try installing the pandoc system package manually: https://pypi.org/project/pypandoc/#installing-pandoc-manually",
                color="pink", is_error=True,
            )
            shell.out("{}".format(error), color="yellow", is_error=True)
            exit(1)

        if verbose:
            shell.out("Running 'pypandoc.convert_file' with the following options:", color="yellow")
            pp(options, width=1)
            shell.out("")

        if not dest:
            shell.out("Converted text...", color="yellow")
            shell.out("")
            shell.out(output)

    @staticmethod
    def _get_pandoc_python_options(source, dest, from_type, to_type, append=False):
        """
        Build the appropriate options for the "pypandoc.convert_file" Python
        command based on the provided parameters.

        See the PyPi package page or the source code for more information.
          - [PyPi](https://pypi.org/project/pypandoc/)
          - [Source](https://github.com/bebraw/pypandoc/blob/master/pypandoc/__init__.py#L104)

        :param source {str}: Path to the file containing text to be converted.
        :param dest {str}:
            (optional) Path to file to write/append converted text.
            If not provided, converted text will output to shell.
            Either the `dest` or `to_type` parameters must be provided.
        :param from_type {str}:
            (optional) The file type to be converted from.
            If not provided, pandoc will guess the type based on file extension.
            Examples: "markdown" or "html"
        :param to_type {str}:
            (optional) The file type to convert into.
            If not provided, pandoc will guess the type based on file extension.
            Either the `dest` or `to_type` parameters must be provided.
            Examples: "html" or "markdown"
        :param append {bool}:
            **NOT IMPLEMENTED**
            If False (by default), the `dest_path` file will be overwritten.
            If True, the description will be appended to the `dest_path` file.
        :return {str}: The "pandoc" conversion command.
        """
        # TODO: Implement append...
        if append:
            shell.out("Appending to existing file is not yet supported. Sorry!", color="yellow")

        return {"source_file": source, "outputfile": dest or None, "format": from_type, "to": to_type}

    @staticmethod
    def _get_pandoc_shell_command(source, dest, from_type, to_type, append=False):
        """
        Build the appropriate "pandoc" shell command based on the provided
        parameters.

        See the [Pandoc Documentation](https://pandoc.org/MANUAL.html) for more
        details.

        ```
        # Command for system-level pandoc package
        cmd = "pandoc {options}".format(
            options=self._get_pandoc_shell_command(source, dest, from_type, to_type, append)
        )
        if verbose:
            shell.out(cmd)
        shell.run(cmd)
        ```

        :param source {str}: Path to the file containing text to be converted.
        :param dest {str}:
            (optional) Path to file to write/append converted text.
            If not provided, converted text will output to shell.
            Either the `dest` or `to_type` parameters must be provided.
        :param from_type {str}:
            (optional) The file type to be converted from.
            If not provided, pandoc will guess the type based on file extension.
            Examples: "markdown" or "html"
        :param to_type {str}:
            (optional) The file type to convert into.
            If not provided, pandoc will guess the type based on file extension.
            Either the `dest` or `to_type` parameters must be provided.
            Examples: "html" or "markdown"
        :param append {bool}:
            **NOT IMPLEMENTED**
            If False (by default), the `dest_path` file will be overwritten.
            If True, the description will be appended to the `dest_path` file.
        :return {str}: The "pandoc" conversion command.
        """
        # TODO: Implement append...
        if append:
            shell.out("Appending to existing file is not yet supported. Sorry!", color="yellow")

        # Convert
        cmd = "pandoc"

        # From this type
        if from_type:
            cmd += " -f {}".format(from_type)

        # Into this type
        if to_type:
            cmd += " -t {}".format(to_type)

        # Using this as the destination file (otherwise output to shell)
        if dest:
            cmd += " -o {}".format(dest)

        # Using this as the source file
        cmd += " {}".format(source)

        return cmd
