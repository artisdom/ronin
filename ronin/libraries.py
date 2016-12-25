# Copyright 2016-2017 Tal Liron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .contexts import current_context
from .utils.types import verify_type

class Library(object):
    """
    Base class for libraries.
    """
    
    def add_to_command(self, command):
        for command_type in command.command_types:
            fn = getattr(self, 'add_to_command_%s' % command_type, None)
            if fn:
                fn(command)

class ExplicitLibrary(Library):
    """
    A library with explicitly stated data.
    """
    
    def __init__(self, include_paths=None, defines=None, library_paths=None, libraries=None):
        super(ExplicitLibrary, self).__init__()
        self.include_paths = include_paths or []
        self.defines = defines or []
        self.library_paths = library_paths or []
        self.libraries = libraries or []

    def add_to_command_gcc_compile(self, command):
        for path in self.include_paths:
            command.add_include_path(path)
        for define, value in self.defines:
            command.define_symbol(define, value)

    def add_to_command_gcc_link(self, command):
        for path in self.library_paths:
            command.add_library_path(path)
        for library in self.libraries:
            command.add_library(library)

class ResultsLibrary(Library):
    """
    A library that pulls results from a build phase.
    """
    
    def __init__(self, phase):
        super(ResultsLibrary, self).__init__()
        from .phases import Phase 
        verify_type(phase, Phase)
        self._phase = phase
    
    def add_to_command_gcc_link(self, command):
        with current_context() as ctx:
            results = ctx.get('_results')
        if results is None:
            return
        results = results.get(self._phase)
        if results is None:
            return
        for result in results:
            command.add_result_library(result)
