$url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$output = "ffmpeg.zip"
$tools_dir = "tools"

# Download FFmpeg
Invoke-WebRequest -Uri $url -OutFile $output

# Extract FFmpeg
Expand-Archive -Path $output -DestinationPath $tools_dir -Force

# Get the extracted folder name (it will have version in the name)
$extracted_dir = Get-ChildItem -Path $tools_dir | Where-Object { $_.PSIsContainer -and $_.Name -like "ffmpeg-*" } | Select-Object -First 1

# Copy ffmpeg.exe to tools directory
Copy-Item "$tools_dir\$($extracted_dir.Name)\bin\ffmpeg.exe" "$tools_dir\ffmpeg.exe" -Force

# Clean up
Remove-Item $output -Force
Remove-Item "$tools_dir\$($extracted_dir.Name)" -Recurse -Force
