import { execSync } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function runDoctor() {
  console.log('\n\x1b[36m=======================================================');
  console.log('   NexusPilot Cortex - Environment Diagnostic Probe    ');
  console.log('=======================================================\x1b[0m\n');

  // 1. Operating System
  const platform = os.platform();
  const release = os.release();
  console.log(`\x1b[32m[✓]\x1b[0m OS: ${platform} (${release}, Architecture: ${os.arch()})`);

  // 2. Python Environment
  let pythonCmd = 'python';
  try {
    const pyVer = execSync('python --version', { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
    console.log(`\x1b[32m[✓]\x1b[0m Python: ${pyVer}`);
  } catch {
    try {
      const pyVer = execSync('py --version', { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
      pythonCmd = 'py';
      console.log(`\x1b[32m[✓]\x1b[0m Python (via py launcher): ${pyVer}`);
    } catch {
      console.log('\x1b[31m[✗]\x1b[0m Python 3.10+ not found on PATH! Please install Python from https://python.org');
    }
  }

  // 3. Core Python Dependencies
  console.log('\n\x1b[36mChecking Python Dependencies for Cortex:\x1b[0m');
  const packages = [
    { name: 'mcp', desc: 'Model Context Protocol SDK', required: true },
    { name: 'sqlite3', desc: 'Embedded Memory Database Engine', required: true },
    { name: 'dataclasses', desc: 'Data Model Serialization', required: true },
    { name: 'tiktoken', desc: 'High-Precision BPE Tokenizer (Optional)', required: false }
  ];

  for (const pkg of packages) {
    try {
      execSync(`${pythonCmd} -c "import ${pkg.name}"`, { stdio: 'ignore' });
      console.log(`  \x1b[32m[✓]\x1b[0m ${pkg.name}: Available (${pkg.desc})`);
    } catch {
      if (pkg.required) {
        console.log(`  \x1b[31m[✗]\x1b[0m ${pkg.name}: Not installed (Run 'pip install ${pkg.name}')`);
      } else {
        console.log(`  \x1b[33m[!]\x1b[0m ${pkg.name}: Not installed (Optional, falling back to built-in heuristic)`);
      }
    }
  }

  // 4. Memory Database Directory Check
  console.log('\n\x1b[36mChecking Cortex Memory Storage:\x1b[0m');
  const localDataDir = path.resolve(__dirname, '..', 'data');
  try {
    if (!fs.existsSync(localDataDir)) {
      fs.mkdirSync(localDataDir, { recursive: true });
    }
    const testFile = path.join(localDataDir, '.probe');
    fs.writeFileSync(testFile, 'probe', 'utf-8');
    fs.unlinkSync(testFile);
    console.log(`  \x1b[32m[✓]\x1b[0m Memory Storage Directory: Writable (${localDataDir})`);
  } catch (err) {
    console.log(`  \x1b[31m[✗]\x1b[0m Memory Storage: Failed to write to ${localDataDir} (${err.message})`);
  }

  console.log('\n\x1b[36m=======================================================');
  console.log(' Diagnostic complete. Ready for NexusPilot Cortex!');
  console.log('=======================================================\x1b[0m\n');
}
