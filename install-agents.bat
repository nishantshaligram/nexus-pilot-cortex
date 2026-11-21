@echo off
setlocal
echo =======================================================
echo    NexusPilot Cortex Multi-Agent MCP Installer
echo =======================================================
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\install-cortex.ps1" %*
echo.
pause
