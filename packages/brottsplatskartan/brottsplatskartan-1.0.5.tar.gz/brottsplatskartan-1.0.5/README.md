# brottsplatskartan [![Build Status](https://travis-ci.com/chrillux/brottsplatskartan.svg?branch=master)](https://travis-ci.com/chrillux/brottsplatskartan)

A simple API wrapper for [Brottsplatskartan](https://brottsplatskartan.se)

## Install

`pip install brottsplatskartan`

## Usage

```python
import brottsplatskartan

b1 = brottsplatskartan.BrottsplatsKartan(app=app, areas=areas)
b2 = brottsplatskartan.BrottsplatsKartan(app=app, longitude=longitude, latitude=latitude)

incidents = b1.get_incidents()
for incident_area in incidents:
    for incident in incidents[incident_area]:
        print(incident)

incidents = b2.get_incidents()
for incident_area in incidents:
    for incident in incidents[incident_area]:
        print(incident)
```

app: unique app value, see https://brottsplatskartan.se/sida/api

areas = Python list of valid areas, see https://brottsplatskartan.se/api/areas

longitude = Longitude

latitude = Latitude

If setting "areas" parameter, longitude and latitude will be ignored.

## Development

Pull requests welcome. Must pass `tox` and include tests.

## Disclaimer

Not affiliated with brottsplatskartan.se. Use at your own risk.
