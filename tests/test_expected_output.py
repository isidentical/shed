"""Update and check saved examples of shed formatting."""

import pathlib
import warnings

import pytest

import shed

from .test_shed import check


@pytest.mark.parametrize(
    "filename", pathlib.Path(__file__).parent.glob("recorded/**/*.txt"), ids=repr
)
def test_saved_examples(filename):
    """Replay and save expected outputs from `shed`.

    To add a file to the test corpus, write it into recorded/foo.txt and
    run the tests; the expected results will be automatically appended
    to the file.

    On test failure, the expected output is automatically updated.
    You can therefore see what changed by examining the `git diff`
    and roll back with `git reset`.
    """
    joiner = "\n\n" + "=" * 80 + "\n\n"
    input_, expected, *_ = map(str.strip, (filename.read_text() + joiner).split(joiner))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", shed.ShedSyntaxWarning)
        result = check(source_code=input_, refactor=True)
    if result.strip() != expected:
        filename.write_text(joiner.join([input_, result]))
        raise AssertionError(filename.name + " changed formatting")
