param(
  [string[]]$Patterns = @(
    "connection refused",
    "could not connect",
    "restart",
    "Traceback",
    "Database"
  )
)

$logs = docker-compose logs --no-color

foreach ($pattern in $Patterns) {
  Write-Host "--- Matches for: $pattern ---"
  $logs | Select-String -Pattern $pattern
}
