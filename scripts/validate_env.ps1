$required = @(
  "POSTGRES_USER",
  "POSTGRES_PASSWORD",
  "POSTGRES_DB",
  "DATABASE_URL",
  "PRODUCT_SERVICE_URL"
)

if (-not (Test-Path ".env")) {
  Write-Error "Missing .env file. Copy .env.example to .env and fill in values."
  exit 1
}

$values = @{}
Get-Content ".env" | ForEach-Object {
  $line = $_.Trim()
  if ($line -eq "" -or $line.StartsWith("#")) { return }
  $parts = $line.Split("=", 2)
  if ($parts.Count -eq 2) {
    $values[$parts[0].Trim()] = $parts[1].Trim()
  }
}

$missing = @()
foreach ($key in $required) {
  if (-not $values.ContainsKey($key) -or [string]::IsNullOrWhiteSpace($values[$key])) {
    $missing += $key
  }
}

if ($missing.Count -gt 0) {
  Write-Error ("Missing or empty values: {0}" -f ($missing -join ", "))
  exit 1
}

Write-Host "Environment validation passed."
