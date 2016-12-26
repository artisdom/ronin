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

from inspect import isclass

def verify_type(value, the_type):
    if not isinstance(value, the_type):
        raise AttributeError('not an instance of %s: %s' % (the_type.__name__, value.__class__.__name__)) 

def verify_subclass(value, the_type):
    if not issubclass(value, the_type):
        raise AttributeError('not a subclass of %s: %s' % (the_type.__name__, value.__name__))

def verify_type_or_subclass(value, the_type):
    if isclass(value):
        verify_subclass(value, the_type)
    else:
        verify_type(value, the_type)