# Clipboard Sentinel — TGDK Hardened Version (QQUAp Encrypted)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Security
Add-Type -AssemblyName System.IO.Compression

$logPath = "$env:APPDATA\TGDK\ClipboardSentinel\logs"
$sentinelLog = "$logPath\clipevents.log"
$encryptionKey = "QQUAp" # Custom encryption key for QQUAp passphrase

# Create log directory
if (!(Test-Path $logPath)) { New-Item -ItemType Directory -Path $logPath -Force | Out-Null }

# QQUAp Encrypt Function
function Encrypt-QQUAp {
    param (
        [string]$plain
    )
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($plain)
    $key = [System.Text.Encoding]::UTF8.GetBytes($encryptionKey.PadRight(32, 'Q'))[0..31]
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Key = $key
    $aes.Mode = "CBC"
    $aes.GenerateIV()
    $encryptor = $aes.CreateEncryptor()
    $cipher = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length)
    return "$([Convert]::ToBase64String($aes.IV))|$([Convert]::ToBase64String($cipher))"
}

# Clipboard Monitor
function Start-ClipboardMonitor {
    $prevClip = ""
    while ($true) {
        try {
            $current = [Windows.Forms.Clipboard]::GetText()
            if ($current -ne $prevClip -and $current -ne "") {
                $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                $encrypted = Encrypt-QQUAp "$timestamp :: Clipboard Changed :: $current"
                Add-Content -Path $sentinelLog -Value $encrypted
                Set-Clipboard -Value ""  # Wipe it instantly
                $prevClip = ""
            }
        } catch { }
        Start-Sleep -Milliseconds 1500
    }
}

# Launch Clipboard Monitor
Start-ClipboardMonitor