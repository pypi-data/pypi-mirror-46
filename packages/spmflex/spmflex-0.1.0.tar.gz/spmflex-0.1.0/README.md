spmflex
=======

Python ≥3.5 driver for [Honeywell SPM Flex gas detectors](https://www.honeywellanalytics.com/en/products/SPM-Flex).

<p align="center">
  <img src="https://www.honeywellanalytics.com/~/media/honeywell-analytics/products/spm-flex/images/spmflex_web_main.jpg" height="400" />
</p>

Installation
============

```
pip install spmflex
```

Usage
=====

### Command Line

To test your connection and stream real-time data, use the command-line
interface. You can read the state with:

```
$ spmflex 192.168.1.100
```

This will output a JSON object which can be further manipulated. See below for
object structure.


### Python

For more complex behavior, you can write a python script. This solely uses
Python ≥3.5's async/await syntax.

```python
import asyncio
from spmflex import GasDetector

async def get():
    async with GasDetector('192.168.1.100') as detector:
        print(await detector.get())

asyncio.run(get())
```

If the detector is operating at that address, this should output a
dictionary of the form:

###
```python
{
    "concentration": 0.0,
    "connected": true,
    "fault": "No fault",
    "flow": 256,
    "gas": "AsH3 - Arsine",
    "high-alarm threshold": "5.0",
    "id": "SPMFLEX08000000",
    "ip": "http://192.168.1.100/",
    "life": 93.0,
    "low-alarm threshold": "2.5",
    "temperature": 0,
    "units": "ppb"
}
```

This is a cleaned-up version of the data returned. If you want to see all of
it, set `raw=True`.
