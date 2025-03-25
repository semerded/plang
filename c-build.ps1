$sourceFolder = "C"
$outputFolder = "src/dll"

if (-not (Test-Path -Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder
}

$sourceFiles = Get-ChildItem -Path $sourceFolder -Filter *.c

if ($sourceFiles.Count -eq 0) {
    Exit 1
}

foreach ($file in $sourceFiles) {
    $outputDll = Join-Path $outputFolder ($file.BaseName + ".dll")
    $command = "gcc -shared -o `"$outputDll`" `"$($file.FullName)`""
    Invoke-Expression $command

    if ($LASTEXITCODE -ne 0) {
        Exit 1
    }   
}
