# MIT License
#
# Copyright (c) 2018 Michael Fuerst
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import re
import json
from importlib import import_module
import inspect
try:
    from jsmin import jsmin
except ModuleNotFoundError:
    def jsmin(x): return x

_sentinel = object()


def import_params(params_file):
    """
    Only libraries should use this method. Human users should directly import their configs.
    Automatically imports the most specific hyperparams from a given file.
    """
    module_name = params_file.replace("\\", ".").replace("/", ".").replace(".py", "")
    module = import_module(module_name)
    symbols = list(module.__dict__.keys())
    symbols = [x for x in symbols if not x.startswith("__") and not x == "HyperParams"]
    n = None
    for x in symbols:
        if not inspect.isclass(module.__dict__[x]):  # in Case we found something that is not a class ignore it.
            continue
        if issubclass(module.__dict__[x], HyperParams):
            # Allow multiple derivatives of hyperparams, when they are derivable from each other in any direction.
            if n is not None and not issubclass(module.__dict__[x], module.__dict__[n]) and not issubclass(module.__dict__[n], module.__dict__[x]):
                raise RuntimeError(
                    "You must only have one class derived from HyperParams in {}. It cannot be decided which to use.".format(params_file))
            # Pick the most specific one if they can be derived.
            if n is None or issubclass(module.__dict__[x], module.__dict__[n]):
                n = x
    if n is None:
        raise RuntimeError("There must be at least one class in {} derived from HyperParams.".format(params_file))
    config = module.__dict__[n]()
    return config


def load_params(filepath):
    """
    Load your hyper parameters from a json file.
    :param filepath: Path to the json file.
    :return: A hyper parameters object.
    """
    print("WARNING: You should switch to using hyperparam python files. Just subclass HyperParams object in a *.py and load it instead of a json.")
    # Read the file
    with open(filepath) as file:
        content = file.read()

    # Finally load hyperparams
    return HyperParams(json.loads(jsmin(content)))


class HyperParams(object):
    """
    Converts a dictionary into an object.
    """

    def __init__(self, d=None):
        """
        Create an object from a dictionary.

        :param d: The dictionary to convert.
        """
        self.immutable = False
        if d is not None:
            for a, b in d.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [HyperParams(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, HyperParams(b) if isinstance(b, dict) else b)

    def to_dict(self):
        return dict((key, value.to_dict()) if isinstance(value, HyperParams) else (key, value)
                    for (key, value) in self.__dict__.items())

    def __repr__(self):
        return "HyperParams(" + self.__str__() + ")"

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    def get(self, key, default=_sentinel):
        """
        Get the value specified in the dictionary or a default.
        :param key: The key which should be retrieved.
        :param default: The default that is returned if the key is not set.
        :return: The value from the dict or the default.
        """
        if default is _sentinel:
            default = HyperParams()
        return self.__dict__[key] if key in self.__dict__ else default

    def __getitem__(self, key):
        """
        Get the value specified in the dictionary or a dummy.
        :param key: The key which should be retrieved.
        :return: The value from the dict or a dummy.
        """
        return self.get(key)

    def __setattr__(self, key, value):
        if "immutable" not in self.__dict__:  # In case users might not call constructor
            self.__dict__["immutable"] = False
        if self.immutable:
            raise RuntimeError("Trying to modify hyperparameters outside constructor.")

        if isinstance(value, str):
            # Try to match linux path style with anything that matches
            for env_var in list(os.environ.keys()):
                s = "$" + env_var
                value = value.replace(s, os.environ[env_var].replace("\\", "/"))

            # Try to match windows path style with anything that matches
            for env_var in list(os.environ.keys()):
                s = "%" + env_var + "%"
                value = value.replace(s, os.environ[env_var].replace("\\", "/"))

            if "%" in value or "$" in value:
                raise RuntimeError("Cannot resove all environment variables used in: '{}'".format(value))
        super.__setattr__(self, key, value)

    def __eq__(self, other):
        if not isinstance(other, HyperParams):
            # don't attempt to compare against unrelated types
            return NotImplemented

        for k in self.__dict__:
            if not k in other.__dict__:
                return False
            if not self.__dict__[k] == other.__dict__[k]:
                return False

        for k in other.__dict__:
            if not k in self.__dict__:
                return False

        return True
