# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2025-05-10

### Added
- Embedded HTTP status dashboard accessible on `/` via configurable host and port.
- Real-time status view with auto-refresh and color-coded health indicators.
- `status_api` block in `config.yaml` to control dashboard behavior.
- Full integration of monitoring loop and HTTP server using `asyncio.gather`.
- Updated documentation with dashboard instructions.

### Fixed
- Parallel execution of monitoring and status server without blocking or deadlocks.
- Logging visibility on server start.

## [0.1.0] - 2025-05-09

### Added
- Docker deployment with persistent configuration and logs.
- Telegram notification support.
- Configurable latency threshold and check intervals.
- Configurable log retention with automatic purging.
- Basic test suite with pytest and pytest-asyncio.
- Example configuration file.
- MIT License.
