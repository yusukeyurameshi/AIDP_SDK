# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to semantic
versioning after the first public release.

## [0.1.0] - 2026-05-28

### Added

- Initial package structure for `ffs-aidp-sdk` with import package `ffs_aidp`.
- OCI signer helpers for config-file, session-token, instance-principal,
  resource-principal and custom signer flows.
- Synchronous HTTP transport based on `requests` with JSON handling, retries,
  timeouts and service-specific exceptions.
- Resource clients for Workspaces, Clusters, Notebooks, Workflows/jobs/job runs,
  Catalogs, Schemas/Tables/Views, Volumes, Delta Share and MLOps preview APIs.
- Pagination helpers and generic waiters for asynchronous/polling workflows.
- Tests, examples, lint/build configuration and UPL-1.0 license.
