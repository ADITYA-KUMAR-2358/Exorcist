$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$env:OLLAMA_MODELS = Join-Path $root ".ollama-models"
$env:OLLAMA_HOST = "127.0.0.1:11434"
$ollama = Join-Path $root "tools\ollama\ollama.exe"

if (-not (Test-Path $ollama)) {
    throw "Ollama is not installed at $ollama"
}

& $ollama serve
