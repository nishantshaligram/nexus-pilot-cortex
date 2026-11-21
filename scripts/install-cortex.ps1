<#
.SYNOPSIS
    NexusPilot Cortex Universal Multi-Agent MCP & Plugin Installer
.DESCRIPTION
    Configures and installs NexusPilot Cortex for Google Antigravity, Claude (Code & Desktop),
    Cursor, Windsurf, and Codex with flexible target flags and interactive selection.
.EXAMPLE
    .\install-cortex.bat -Antigravity
    .\install-cortex.bat -Claude -Cursor
    .\install-cortex.bat -Target Antigravity
    .\install-cortex.bat --all
#>

[CmdletBinding()]
param(
    [Alias("Target")]
    [string[]]$TargetAgent,

    [switch]$Antigravity,
    [switch]$Claude,
    [switch]$Cursor,
    [switch]$Windsurf,
    [switch]$All,
    [switch]$NonInteractive
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = (Split-Path -Parent $ScriptDir).Replace("\", "/")
$ServerScript = "$ProjectRoot/server/cortex_server.py"
$RegisterScript = "$ScriptDir/register_mcp.py"

# Detect Python executable
$PyExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $PyExe) {
    $PyExe = "python"
} else {
    $PyExe = $PyExe.Replace("\", "/")
}

Write-Host "`n=======================================================" -ForegroundColor Cyan
Write-Host "   NexusPilot Cortex Universal MCP & Plugin Installer  " -ForegroundColor Cyan
Write-Host "   (Telemetry, Memory Governor & Context Compressor)   " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "Project Root : $ProjectRoot" -ForegroundColor Gray
Write-Host "Server Script: $ServerScript" -ForegroundColor Gray
Write-Host "Python Binary: $PyExe`n" -ForegroundColor Gray

# Collect targets from flags or posix arguments
$SelectedTargets = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)

# 1. Parse switch parameters
if ($All) {
    @("Antigravity", "Claude", "Cursor", "Windsurf") | ForEach-Object { [void]$SelectedTargets.Add($_) }
}
if ($Antigravity) { [void]$SelectedTargets.Add("Antigravity") }
if ($Claude)      { [void]$SelectedTargets.Add("Claude") }
if ($Cursor)      { [void]$SelectedTargets.Add("Cursor") }
if ($Windsurf)    { [void]$SelectedTargets.Add("Windsurf") }

# 2. Parse -Target / -TargetAgent
if ($TargetAgent) {
    foreach ($t in $TargetAgent) {
        $parts = $t -split "[,;\s]+"
        foreach ($p in $parts) {
            $clean = $p.Trim()
            if ($clean -eq "All") {
                @("Antigravity", "Claude", "Cursor", "Windsurf") | ForEach-Object { [void]$SelectedTargets.Add($_) }
            } elseif ($clean) {
                [void]$SelectedTargets.Add($clean)
            }
        }
    }
}

# 3. Parse remaining POSIX-style arguments (--antigravity, --claude, etc.)
foreach ($arg in $args) {
    switch -Regex ($arg) {
        "^--?all$"         { @("Antigravity", "Claude", "Cursor", "Windsurf") | ForEach-Object { [void]$SelectedTargets.Add($_) } }
        "^--?(agy|antigravity)$" { [void]$SelectedTargets.Add("Antigravity") }
        "^--?claude$"      { [void]$SelectedTargets.Add("Claude") }
        "^--?cursor$"      { [void]$SelectedTargets.Add("Cursor") }
        "^--?windsurf$"    { [void]$SelectedTargets.Add("Windsurf") }
    }
}

# 4. Interactive prompt if no target was specified
if ($SelectedTargets.Count -eq 0) {
    if ($NonInteractive) {
        # Default to All if non-interactive
        @("Antigravity", "Claude", "Cursor", "Windsurf") | ForEach-Object { [void]$SelectedTargets.Add($_) }
    } else {
        Write-Host "No target environment specified. Choose an option:" -ForegroundColor Yellow
        Write-Host "  [1] All (Antigravity, Claude, Cursor, Windsurf) [Default]"
        Write-Host "  [2] Google Antigravity Only"
        Write-Host "  [3] Claude Only (Desktop & Code CLI)"
        Write-Host "  [4] Cursor IDE Only"
        Write-Host "  [5] Windsurf Only"
        Write-Host "  [6] Antigravity + Claude Only`n"
        
        $choice = Read-Host "Enter choice [1-6] (Press Enter for 1)"
        switch ($choice.Trim()) {
            "2" { [void]$SelectedTargets.Add("Antigravity") }
            "3" { [void]$SelectedTargets.Add("Claude") }
            "4" { [void]$SelectedTargets.Add("Cursor") }
            "5" { [void]$SelectedTargets.Add("Windsurf") }
            "6" { [void]$SelectedTargets.Add("Antigravity"); [void]$SelectedTargets.Add("Claude") }
            default {
                @("Antigravity", "Claude", "Cursor", "Windsurf") | ForEach-Object { [void]$SelectedTargets.Add($_) }
            }
        }
        Write-Host ""
    }
}

$TargetList = ($SelectedTargets | ForEach-Object { $_ }) -join ", "
Write-Host "Target Environments Selected: " -NoNewline -ForegroundColor White
Write-Host "$TargetList`n" -ForegroundColor Green

function Update-McpConfigFile {
    param(
        [string]$FilePath,
        [string]$AgentName
    )

    try {
        & $PyExe "$RegisterScript" "$FilePath" "nexus-pilot-cortex" --command "$PyExe" --script "$ServerScript" --description "NexusPilot Cortex Telemetry, Memory & Context Compressor Engine"
        Write-Host "    [x] Configured $AgentName successfully!" -ForegroundColor Green
        Write-Host "        Config: $FilePath" -ForegroundColor Gray
    } catch {
        Write-Host "    [-] Failed to configure $AgentName`: $_" -ForegroundColor Red
    }
}

# 1. Antigravity Installation
if ($SelectedTargets.Contains("Antigravity")) {
    Write-Host "[•] Installing for Google Antigravity..." -ForegroundColor Cyan
    $PluginTargetDir = "$HOME/.gemini/config/plugins/nexus-pilot-cortex"
    try {
        if (-not (Test-Path $PluginTargetDir)) {
            New-Item -ItemType Directory -Path $PluginTargetDir -Force | Out-Null
        }
        # Copy plugin contents gracefully (avoiding failures if runtime files are locked)
        Get-ChildItem -Path $ProjectRoot -Exclude "data", "__pycache__" | ForEach-Object {
            try {
                Copy-Item -Path $_.FullName -Destination $PluginTargetDir -Recurse -Force -ErrorAction SilentlyContinue
            } catch {
                Write-Host "    [!] Notice: $($_.Name) is currently locked by a running process; keeping existing copy." -ForegroundColor Yellow
            }
        }
        Write-Host "    [x] Plugin bundle installed in: $PluginTargetDir" -ForegroundColor Green

        # Also configure global Antigravity MCP server entry
        $AgyMcpPath = "$HOME/.gemini/antigravity/mcp_config.json"
        Update-McpConfigFile -FilePath $AgyMcpPath -AgentName "Antigravity Global MCP"
    } catch {
        Write-Host "    [-] Antigravity plugin installation failed: $_" -ForegroundColor Red
    }
}

# 2. Claude (Claude Code & Claude Desktop)
if ($SelectedTargets.Contains("Claude")) {
    Write-Host "`n[•] Installing for Claude..." -ForegroundColor Cyan
    # A. Claude Code CLI (~/.claude.json)
    $ClaudeCodePath = "$HOME/.claude.json"
    Update-McpConfigFile -FilePath $ClaudeCodePath -AgentName "Claude Code CLI"

    # B. Claude Desktop App (%APPDATA%\Claude\claude_desktop_config.json)
    $ClaudeDesktopPath = "$env:APPDATA/Claude/claude_desktop_config.json"
    Update-McpConfigFile -FilePath $ClaudeDesktopPath -AgentName "Claude Desktop App"
}

# 3. Cursor IDE
if ($SelectedTargets.Contains("Cursor")) {
    Write-Host "`n[•] Installing for Cursor IDE..." -ForegroundColor Cyan
    $CursorMcpPath = "$HOME/.cursor/mcp.json"
    Update-McpConfigFile -FilePath $CursorMcpPath -AgentName "Cursor Global MCP"
}

# 4. Windsurf / Codeium
if ($SelectedTargets.Contains("Windsurf")) {
    Write-Host "`n[•] Installing for Windsurf / Codeium..." -ForegroundColor Cyan
    $WindsurfPath = "$HOME/.codeium/windsurf/mcp_config.json"
    Update-McpConfigFile -FilePath $WindsurfPath -AgentName "Windsurf Global MCP"
}

Write-Host "`n=======================================================" -ForegroundColor Cyan
Write-Host "   Installation Complete for: $TargetList!              " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
