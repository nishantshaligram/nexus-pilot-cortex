# Contributing to NexusPilot Cortex

Thank you for your interest in contributing to **NexusPilot Cortex**!  
Cortex is an open-source cognitive middleware providing AI agents with real-time token telemetry badging, persistent long-term memory (*claude-mem* parity), and adaptive context compression (*headroom* parity).

---

## 🛠️ Development Setup

### 1. Prerequisites
- Python 3.10+ (Standard library, 0 required external dependencies)
- Node.js 18+ (For NPX CLI and VitePress documentation)
- Git

### 2. Clone and Setup
```bash
git clone https://github.com/nishantshaligram/nexus-pilot-cortex.git
cd nexus-pilot-cortex
```

### 3. Run Environment Diagnostics
```bash
node ./bin/nexus-pilot-cortex.js doctor
```

### 4. Run Automated Test Suite
```bash
python tests/run_tests.py -v
```

---

## 🚀 Contribution Workflow

1. **Fork & Branch:** Create a feature branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. **Follow Code Conventions:**
   - Python: Clean type annotations, standard library priority, zero mandatory external dependencies.
   - Node.js: ES Module (`type: module`), cross-platform paths (`path.join` / POSIX normalization).
3. **Write Tests:** Ensure all tests pass with `python tests/run_tests.py` and add unit tests for new capabilities in `tests/test_cortex.py`.
4. **Conventional Commits:** Use clear commit prefixes (`feat:`, `fix:`, `docs:`, `test:`, `perf:`).
5. **Open a Pull Request:** Provide a clear description of the problem solved and test verification output.
