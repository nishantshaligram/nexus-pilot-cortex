# Security Policy

## Responsible Disclosure

The NexusPilot team takes security, privacy, and system integrity seriously. Because NexusPilot Cortex manages persistent memory, context compression, and sensitive operational telemetry, we enforce strict local-first safety guarantees:

- **100% Local-First Storage:** All memories, telemetry ledgers, and compressed cache representations remain on your local disk (`~/.gemini/plugins/nexus-pilot-cortex/data/` or project data). Zero third-party cloud telemetry or exfiltration.
- **PII & Credential Filtering:** Heuristic extractors ignore API tokens, private keys, passwords, and authorization headers from autonomous memory extraction.

If you discover a security vulnerability or credential leak risk in NexusPilot Cortex, please report it privately:

- **Email:** nishant.shaligram@gmail.com
- Please include steps to reproduce, affected version, and your environment details.
- We aim to acknowledge receipt within 48 hours and provide a remediation timeline.

Please do not open public GitHub issues for undisclosed security vulnerabilities.
