from types import SimpleNamespace

import pytest

import fastentrypoints


def test_distribution_requirement_uses_as_requirement_when_available():
    dist = SimpleNamespace(as_requirement=lambda: 'thefuck==0.4.0')

    assert fastentrypoints._distribution_requirement(dist) == 'thefuck==0.4.0'


def test_distribution_requirement_falls_back_to_metadata():
    metadata = {'Name': 'thefuck', 'Version': '0.4.0'}
    dist = SimpleNamespace(project_name=None, name=None, version=None, metadata=metadata)

    assert fastentrypoints._distribution_requirement(dist) == 'thefuck==0.4.0'


def test_get_args_falls_back_to_original_writer_for_dist_without_entry_map(mocker):
    expected = [('script.py', 'print(123)', 't')]
    original = mocker.patch('fastentrypoints._original_get_args', return_value=iter(expected))

    result = list(
        fastentrypoints.easy_install.ScriptWriter.get_args(
            SimpleNamespace(), header='hdr'
        )
    )

    assert result == expected
    original.assert_called_once()


def test_get_args_rejects_script_names_with_path_separator():
    entry_point = SimpleNamespace(module_name='thefuck.entrypoints.main', attrs=['main'])
    dist = SimpleNamespace(
        get_entry_map=lambda _group: {'bad/name': entry_point},
        as_requirement=lambda: 'thefuck==0.4.0',
    )

    with pytest.raises(ValueError):
        list(
            fastentrypoints.easy_install.ScriptWriter.get_args(dist, header='hdr')
        )
