$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open('d:\My work\workshop\prompt-engineering-workshop\materials\Prompt_Engineering_Workshop_v2.pptx', $true, $false, $false)
Write-Output "PowerPoint COM Opened successfully! Total Slides: $($pres.Slides.Count)"
$pres.Close()
