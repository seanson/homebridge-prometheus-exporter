# homebridge-prometheus-exporter

- Chart can be found at github [seanson/homebridge-prometheus-exporter](https://github.com/seanson/homebridge-prometheus-exporter)

### Installation

```bash
$ helm repo add homebridge-prometheus-exporter https://seanson.github.io/homebridge-prometheus-exporter
$ helm install homebridge-prometheus-exporter/homebridge-prometheus-exporter
```

![Version: 0.2.0](https://img.shields.io/badge/Version-0.2.0-informational?style=flat-square)

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| homebridge.credentials | object | `{"password":"","username":""}` | Username and password for HomeBridge API authentication |
| homebridge.sealedCredentials | object | `{"password":"","username":""}` | Optional sealed secret for credentials, can be set if you run the SealedSecrets controller  |
| homebridge.url | string | `""` | URL of the target HomeBridge API instace to hit |
| image.pullPolicy | string | `"Always"` |  |
| image.repository | string | `"ghcr.io/seanson/homebridge-prometheus-exporter"` |  |
| livenessProbe.failureThreshold | int | `10` |  |
| livenessProbe.httpGet.path | string | `"/metrics"` |  |
| livenessProbe.httpGet.port | int | `5000` |  |
| livenessProbe.initialDelaySeconds | int | `30` |  |
| livenessProbe.timeoutSeconds | int | `10` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| readinessProbe.httpGet.path | string | `"/metrics"` |  |
| readinessProbe.httpGet.port | int | `5000` |  |
| resources | object | `{}` |  |
| service.enabled | bool | `true` |  |
| service.port | int | `80` |  |
| service.targetport | int | `5000` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `nil` |  |
| serviceMonitor.enabled | bool | `false` |  |
| serviceMonitor.interval | string | `"30s"` |  |
| serviceMonitor.path | string | `"/metrics"` |  |
| serviceMonitor.scrapeTimeout | string | `"10s"` |  |
| tolerations | list | `[]` |  |

## Development

### Requirements

Install the Helm plugin for managing versions:

```bash
helm plugin install https://github.com/mbenabda/helm-local-chart-version
```

### Releases

Releases are automatically published by GitHub actions on push of a new chart version.

Note: If the GitHub release succeeds but the publish fails for some reason it will not re-attempt until the GitHub release and tag is deleted.

### Helm Development

Charts should be developed with Helm3 compatability in mind with Kubernetes 1.19 as the target for API versioning.

### Chart Versioning

All charts should share the same semantic versioning with backwards compatability based on users having to change their `values.yaml` structures. Versions should be changed in `Chart.yaml`, the header of this `README.md`, given a git tag. Changes should be documented in `CHANGELOG.md`.

Please use one of the following `make` targets to bump versions:

Backwards compatible change:

```bash
make bump-patch
```

Backwards compatible but minor changes required (Please add to CHANGELOG.md!)

```bash
make bump-minor
```

Major incomaptible changes, expectation to uninstall and reinstall (Please add to CHANGELOG.md!)

```bash
make bump-major
```

### Documentation

Chart documentation is generated via [helm-docs](https://github.com/norwoodj/helm-docs) and templated via README.md.gotmpl. Once generated they are then formatted with the VS Code default markdown formatter.
