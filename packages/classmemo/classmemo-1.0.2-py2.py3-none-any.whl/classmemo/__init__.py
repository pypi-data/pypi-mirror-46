"""
A `Memoizer` can be used as a factory for creating objects of a certain class.
It exposes a constructor and 2 methods

* `memoizer = Memoizer(SomeClass)`
* `memoizer.get(*args, **kwargs)`
    * If `memoizer` has never seen the given arguments, it creates `SomeClass(*args, **kwargs)` and returns it.
    * If `memoizer` has seen the given arguments before, it returns the same instance that it returned the last time.
* `memoizer.forget(*args, **kwargs)`
    * Makes `memoizer` forget that is has seen the given arguments.

### Usage

The original application was for a `MeasurementQueue` class that processes incoming sensor data from many sensors,
where the sensor ID's were not known ahead of time:

```python
queue_manager = Memoizer(MeasurementQueue)

for sensor_id, data in event_stream():
    queue = queue_manager.get(sensor_id)
    queue.push(data)
```

When the first measurement comes in for a given sensor_id, a new `MeasurementQueue` will be created and returned for
that sensor. On subsequent events with the same sensor ID, the same `MeasurementQueue` instance will be
used to process the data.
"""
from typing import Tuple

from frozendict import frozendict


class Memoizer(object):
    __slots__ = ["instances", "cls"]

    def __init__(self, cls: type):
        """Set the class and make an empty instance dict"""
        self.instances = {}
        self.cls = cls

    def key(self, *args, **kwargs) -> Tuple[Tuple, frozendict]:
        """Returns the arguments as a key that can be used for dictionary lookup."""
        return (args, frozendict(kwargs))

    def get(self, *args, **kwargs):
        """Returns an instance if found, otherwise a new instance."""
        key = self.key(*args, **kwargs)
        if key not in self.instances:
            self.instances[key] = self.cls(*args, **kwargs)
        return self.instances[key]

    def forget(self, *args, **kwargs):
        """Removes the instance from the internal lookup."""
        key = self.key(*args, **kwargs)
        self.instances.pop(key, None)
