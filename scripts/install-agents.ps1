<#
.SYNOPSIS
    NexusPilot Cortex Universal Multi-Agent MCP & Plugin Installer
.DESCRIPTION
    Alias matching NexusPilot Desktop's install-agents.ps1
#>

param(
    [ValidateSet("All", "Antigravity", "Claude", "Cursor", "Windsurf")]
    [string]$TargetAgent = "All"
)

& "$PSScriptRoot/install-cortex.ps1" -TargetAgent $TargetAgent
