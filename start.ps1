$ErrorActionPreference = "Stop"

function Confirm-Action {
    param(
        [string]$Message
    )

    while ($true) {
        $answer = Read-Host "$Message [y/n]"

        switch ($answer.ToLower()) {
            "y" { return $true }
            "n" { return $false }
            default {
                Write-Host "Please enter y or n."
            }
        }
    }
}

Set-Location $PSScriptRoot

if (Confirm-Action "Run pytest?") {
    uv run --no-sync pytest -v

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Tests failed. Bot startup cancelled."
        exit 1
    }

    Write-Host "All tests passed."
}
else {
    if (-not (Confirm-Action "Skip tests and start bot?")) {
        Write-Host "Bot startup cancelled."
        exit 0
    }

    Write-Warning "Starting bot without running tests."
}

uv run --no-sync python src/bot.py

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
