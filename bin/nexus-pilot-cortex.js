#!/usr/bin/env node

import { startMcpServer } from '../src/server-runner.js';
import { runInstaller } from '../src/installer.js';
import { runDoctor } from '../src/doctor.js';

const args = process.argv.slice(2);
const command = args[0]?.toLowerCase();

function printHelp() {
  console.log(`
NexusPilot Cortex - Cognitive Telemetry, Memory & Context Compressor Suite

Usage:
  npx nexus-pilot-cortex                          Start the MCP server daemon over stdio (default)
  npx nexus-pilot-cortex serve                    Explicitly run the MCP server daemon
  npx nexus-pilot-cortex install [options]        Install plugin & skills into AI agent configs
  npx nexus-pilot-cortex doctor                   Run environment & SQLite diagnostics
  npx nexus-pilot-cortex --help                   Show this help message
  npx nexus-pilot-cortex --version                Show package version

Install Options:
  --agent <name>       Target agent to configure: all, antigravity, claude, cursor, windsurf
  --ide <name>         Alias for --agent (e.g. --ide cursor)

Examples:
  npx nexus-pilot-cortex install
  npx nexus-pilot-cortex install --agent antigravity
  npx nexus-pilot-cortex install --ide claude
  npx nexus-pilot-cortex doctor
`);
}

function parseFlag(flagName) {
  const idx = args.indexOf(flagName);
  if (idx !== -1 && args[idx + 1] && !args[idx + 1].startsWith('-')) {
    return args[idx + 1];
  }
  const inline = args.find(a => a.startsWith(`${flagName}=`));
  if (inline) {
    return inline.split('=')[1];
  }
  return null;
}

switch (command) {
  case 'install': {
    const target = parseFlag('--agent') || parseFlag('--ide');
    await runInstaller(target);
    break;
  }
  case 'doctor':
    runDoctor();
    break;
  case 'serve':
    startMcpServer();
    break;
  case '--help':
  case '-h':
  case 'help':
    printHelp();
    break;
  case '--version':
  case '-v':
    console.log('nexus-pilot-cortex v1.0.0');
    break;
  default:
    // When invoked with no args or unrecognized flag, start the MCP server directly
    startMcpServer();
    break;
}
