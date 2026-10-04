$src = 'd:\My work\workshop\prompt-engineering-workshop\materials\Prompt_Engineering_Workshop_v2.pptx'
$out = 'C:\Users\Mahdi\.gemini\antigravity\brain\df94e5f5-defe-4483-8f42-56cd29c83cca\scratch'
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open($src, $true, $false, $false)
foreach ($i in 14, 15) {
    $pres.Slides.Item($i).Export("$out\slide_$i.png", 'PNG', 1600, 900)
}
$pres.Close()
$app.Quit()
Write-Output 'Exported successfully'
