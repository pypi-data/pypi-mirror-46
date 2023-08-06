import re

from . import utils


COPYRIGHT = '\n'.join([
    r"Copyright \(c\) 20\d{2} Celadon Development LLC, All rights reserved.",
    r"Author \w+ \w+ <\w+\.\w+@celadon.ae>",
])


def _comment_copyright(copyright, comment_symbol):
    copyright_lines = copyright.split('\n')
    commented_copyrights_lines = [
        ' '.join([comment_symbol, line])
        for line in copyright_lines
    ]
    return '\n'.join(commented_copyrights_lines)


COPYRIGHT_BY_FILE_EXTENSION = {
    'js': _comment_copyright(COPYRIGHT, '//'),
    'py': _comment_copyright(COPYRIGHT, '#'),
}


def get_file_copyright(file_path):
    file_extension = file_path.split('.')[-1]
    return COPYRIGHT_BY_FILE_EXTENSION[file_extension]


class LintingError(ValueError):
    def __init__(self, errors):
        if isinstance(errors, (list, tuple)):
            error_files = '\n'.join(errors)
        else:
            error_files = errors

        error_message = 'Failed linting such files:\n {}'.format(error_files)
        super().__init__(error_message)


def lint_project(workdir, config):
    failed_liniting_files = []
    for file_path in utils.walk_files_recursively(workdir):
        if not utils.is_ignore_file(file_path, config.ignores):
            try:
                lint_file(file_path)
            except LintingError:
                failed_liniting_files.append(file_path)
            except Exception:
                pass

    if failed_liniting_files:
        raise LintingError(failed_liniting_files)


def lint_file(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
        copyright_re = re.compile(get_file_copyright(file_path), re.MULTILINE)
        if copyright_re.search(source_code) is None:
            raise LintingError(file_path)
