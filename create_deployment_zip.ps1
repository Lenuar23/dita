# PowerShell script to prepare ZIP archive for Wispbyte
# Run this in PowerShell as administrator

# Parameters
$projectPath = "d:\Dota tool box\Onibi"
$outputZip = "d:\Dota tool box\onibi-parser.zip"

# Files to include
$includeFiles = @(
    "config.py",
    "main.py",
    "steam_parser.py",
    "telegram_bot.py",
    "requirements.txt",
    "Dockerfile",
    "README.md",
    "DEPLOYMENT.md",
    "DEPLOYMENT_NO_GITHUB.md",
    "test_deployment.py",
    ".env"
)

# Папки які потрібно включити
$includeFolders = @()

# Видалимо старий ZIP якщо існує
if (Test-Path $outputZip) {
    Remove-Item $outputZip -Force
    Write-Host "✅ Старий архів видалено"
}

# Перейдемо до папки проекту
cd $projectPath

# Створимо тимчасову папку для архіву
$tempDir = "$projectPath\temp_archive"
if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null
Write-Host "✅ Тимчасова папка створена"

# Копіюємо файли
foreach ($file in $includeFiles) {
    $filePath = "$projectPath\$file"
    if (Test-Path $filePath) {
        Copy-Item $filePath -Destination $tempDir
        Write-Host "✅ Додано: $file"
    } else {
        Write-Host "⚠️  Не знайдено: $file"
    }
}

# Копіюємо папки
foreach ($folder in $includeFolders) {
    $folderPath = "$projectPath\$folder"
    if (Test-Path $folderPath) {
        Copy-Item $folderPath -Destination $tempDir -Recurse
        Write-Host "✅ Додано папку: $folder"
    }
}

# Створюємо ZIP архів
Write-Host ""
Write-Host "📦 Створюємо архів..."
Compress-Archive -Path $tempDir -DestinationPath $outputZip -Force

# Видаляємо тимчасову папку
Remove-Item $tempDir -Recurse -Force
Write-Host "✅ Тимчасова папка видалена"

# Інформація про архів
$fileSize = (Get-Item $outputZip).Length / 1MB
Write-Host ""
Write-Host "=========================================="
Write-Host "✅ АРХІВ ГОТОВИЙ!"
Write-Host "=========================================="
Write-Host "Шлях: $outputZip"
Write-Host "Розмір: $([Math]::Round($fileSize, 2)) MB"
Write-Host ""
Write-Host "Наступні кроки:"
Write-Host "1. Перейдіть на Wispbyte панель"
Write-Host "2. Перейдіть до Files → Upload Files"
Write-Host "3. Виберіть цей ZIP архів"
Write-Host "4. Розархівуйте: unzip onibi-parser.zip"
Write-Host "5. Встановіть залежності: pip install -r requirements.txt"
Write-Host "6. Запустіть: python main.py"
Write-Host "=========================================="
