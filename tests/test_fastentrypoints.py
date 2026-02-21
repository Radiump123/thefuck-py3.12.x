from types import SimpleNamespace

import pytest

import fastentrypoints


def test_distribution_requirement_uses_as_requirement_when_available():
    dist = SimpleNamespace(as_requirement=lambda: 'thefuck==4.1')

    assert fastentrypoints._distribution_requirement(dist) == 'thefuck==4.1'


def test_distribution_requirement_falls_back_to_metadata():
    metadata = {'Name': 'thefuck', 'Version': '4.1'}
    dist = SimpleNamespace(project_name=None, name=None, version=None, metadata=metadata)

    assert fastentrypoints._distribution_requirement(dist) == 'thefuck==4.1'


from types import SimpleNamespace
from setuptools.command.easy_install import ScriptWriter

def test_get_args_fallback_for_dist_without_entry_map():
    """
    Ensure ScriptWriter.get_args works for distributions without an entry map.
    """
    # a "dist" without entry points
    dist = SimpleNamespace(get_entry_map=lambda _: {})

    # call get_args and convert to a list
    result = list(ScriptWriter.get_args(dist, header='hdr'))

    # verify it returns a list of tuples (script_name, body, type) like the original test expected
    # the pytest worked, i actually managed to fix this junk!
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 3

def test_get_args_rejects_script_names_with_path_separator():
    entry_point = SimpleNamespace(module_name='thefuck.entrypoints.main', attrs=['main'])
    dist = SimpleNamespace(
        get_entry_map=lambda _group: {'bad/name': entry_point},
        as_requirement=lambda: 'thefuck==4.1',
    )

    with pytest.raises(ValueError):
        list(
            fastentrypoints.easy_install.ScriptWriter.get_args(dist, header='hdr')
        )
