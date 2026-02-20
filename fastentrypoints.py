# Copyright (c) 2016, Aaron Christianson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
Monkey patch setuptools to write faster console_scripts with this format:

    import sys
    from mymodule import entry_function
    sys.exit(entry_function())

This is better.

(c) 2016, Aaron Christianson
http://github.com/ninjaaron/fast-entry_points
'''
import warnings

from setuptools.command import easy_install
from setuptools.warnings import SetuptoolsDeprecationWarning
import re

_original_get_args = None

# Silence setuptools deprecation noise for legacy easy_install access in this shim.
warnings.filterwarnings(
    "ignore",
    message=r".*setuptools\.command\.easy_install.*",
    category=SetuptoolsDeprecationWarning,
)
TEMPLATE = r'''\
# -*- coding: utf-8 -*-
# EASY-INSTALL-ENTRY-SCRIPT: '{3}','{4}','{5}'
__requires__ = '{3}'
import re
import sys

from {0} import {1}

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit({2}())'''


def _distribution_requirement(dist):
    """Return a requirement-like string for setuptools script metadata."""
    as_requirement = getattr(dist, 'as_requirement', None)
    if callable(as_requirement):
        return str(as_requirement())

    metadata = getattr(dist, 'metadata', None)
    name = getattr(dist, 'project_name', None) or getattr(dist, 'name', None)
    version = getattr(dist, 'version', None)

    if metadata is not None:
        get_meta = getattr(metadata, 'get', None)
        if callable(get_meta):
            name = name or get_meta('Name')
            version = version or get_meta('Version')

    if name and version:
        return f'{name}=={version}'
    return name or ''

@classmethod
def get_args(cls, dist, header=None):
    """Yield write_script() argument tuples for script entry points."""
    if header is None:
        header = cls.get_header()

    if not hasattr(dist, 'get_entry_map'):
        for res in _original_get_args(dist, header):
            yield res
        return

    spec = _distribution_requirement(dist)
    for type_ in 'console', 'gui':
        group = type_ + '_scripts'
        for name, ep in dist.get_entry_map(group).items():
            if re.search(r'[\\/]', name):
                raise ValueError("Path separators not allowed in script names")
            script_text = TEMPLATE.format(
                ep.module_name, ep.attrs[0], '.'.join(ep.attrs),
                spec, group, name)
            for res in cls._get_script_args(type_, name, header, script_text):
                yield res


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    _original_get_args = easy_install.ScriptWriter.get_args
    easy_install.ScriptWriter.get_args = get_args


def main():
    import os
    import re
    import shutil
    import sys
    dests = sys.argv[1:] or ['.']
    filename = re.sub(r'\.pyc$', '.py', __file__)

    for dst in dests:
        shutil.copy(filename, dst)
        manifest_path = os.path.join(dst, 'MANIFEST.in')
        setup_path = os.path.join(dst, 'setup.py')

        # Insert the include statement to MANIFEST.in if not present
        with open(manifest_path, 'a+') as manifest:
            manifest.seek(0)
            manifest_content = manifest.read()
            if not 'include fastentrypoints.py' in manifest_content:
                manifest.write(('\n' if manifest_content else '')
                               + 'include fastentrypoints.py')

        # Insert the import statement to setup.py if not present
        with open(setup_path, 'a+') as setup:
            setup.seek(0)
            setup_content = setup.read()
            if not 'import fastentrypoints' in setup_content:
                setup.seek(0)
                setup.truncate()
                setup.write('import fastentrypoints\n' + setup_content)

