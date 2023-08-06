## Memoizer

### API

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

## Installation

I will try to make it available as a package.

For now, a local copy can be installed by cloning the repo and running `pip install -r requirements.txt`.
The only dependencies are Python 3.6 and the frozendict package.

## Contributing

* Ensure the tests pass: `pytest .`
* Format the code with `black . -t py36`
