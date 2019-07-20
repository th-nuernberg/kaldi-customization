Get-Content -Path .\config\.env | ForEach-Object -Process {
    $line = $_.Trim()
    if (-not ([string]::IsNullOrWhiteSpace($line))) {
        $varName = ($line -split '=')[0]
        $varValue = ($line -split '=')[1]
        New-Item -Path env:\$varName -Value $varValue
    }
}