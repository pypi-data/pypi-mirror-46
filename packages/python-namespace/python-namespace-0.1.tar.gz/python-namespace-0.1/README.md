# Introduction

The namespace decorator can be used to automatically instantiate inner classes.

Inner classes are used to group functionality. The namespace decorator simplifies their use and
provides some useful auxilliary attributes.


# Example

## Class definition

```
from namespace import Namespace


class Scope(SomeBaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._channel_count = 4  # number of channels

    @Namespace
    class measurement:
        @property
        def status(self):
            # the root property can be used to access the root class instance, here "Scope"
            return self.root.send_command('status')

    @Namespace
    class acquisition:
        def start(self):
            self.root.send_command('acquisition:start')

    # repeat with a soft coded number of channels
    @Namespace.repeat('_channel_count')
    class channels:
        @property
        def offset(self):
            # In a repeated namespace the "index" property can be used to determine the
            # index of the instance in the list
            return self.root.send_command('channel{0}:offset?'.format(self.index))

        @offset.setter
        def offset(self, value):
            self.root.send_command('channel{0}:offset {1}'.format(self.index, value))

    # Namespace.repeat with a hardcoded number of repetitions
    @Namespace.repeat(2)
    class trigger:
        @Namespace
        class edge:
            @property
            def level(self):
                # For nested namespaces the parent namespace can be accessed with the "parent" property
                return self.root.send_command('trigger{0}:edge:level?'.format(self.parent.index))

            @level.setter
            def level(self, value):
                self.root.send_command('trigger{0}:edge:level {1}'.format(self.parent.index, value))

```

## Usage

```
# instantiate class
scope = Scope()
# print the status which is a property of the measurement namespace.
print(scope.measurement.status)
# set the offset of the 1st channel. channels is a repeated namespace.
scope.channels[0].offset = 3
# Set trigger level. The edge namespace is a child namespace of the trigger namespace.
scope.trigger[0].edge.level = 5
# start acquisition. start() is a method of the acquisition namespace.
scope.acquisition.start()
```

## Attributes

A namespace has the following attributes

- `root`: link to the class object.
- `parent`: link to the parent namespace

Repeated namespaces have furthermore the following attributes

- `index`: the index of the namespace in the list of the repeated namespaces.


# Requirements

- Python 3

# Installation

```
python setup.py install
```

or

```
pip install python-namespace
```
