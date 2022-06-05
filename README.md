# homebridge-prometheus-exporter

This is a small exporter that pulls data from the [HomeBridge API](https://homebridge.io/) to provide accessory information as a Prometheus metric.

It is installable as a Helm chart -- see the [README](./charts/homebridge-prometheus-exporter) for installation instructions.

## Configuration

This requires the following env vars:
- `HOMEKIT_USERNAME` - Username for authentication against the HomeBridge API
- `HOMEKIT_PASSWORD` - Password for authentication against the HomeBridge API
- `HOMEKIT_URL` - The URL for querying to export metrics
