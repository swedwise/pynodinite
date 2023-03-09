<#
.SYNOPSIS
Makes a POST request to a specified URL, sending the contents of a specified JSON file as data.

.DESCRIPTION
This script uses the Invoke-WebRequest cmdlet to send a POST request to the specified URL, sending the contents of a specified JSON file as data. The script is compatible with PowerShell versions running on Windows Server 2017.

.PARAMETER BaseUrl
The base URL to which the POST request should be sent. This should not include the endpoint path (e.g. /LogAPI/api/logevent), which is added automatically by the script.

.PARAMETER JsonFilePath
The path to the JSON file to be sent as data in the POST request.

.EXAMPLE
.\SendFileToLogAPI.ps1 -BaseUrl "https://example.com" -JsonFilePath "C:\path\to\file.json"

This example sends the contents of the C:\path\to\file.json file as data in a POST request to the https://example.com/LogAPI/api/logevent endpoint.

.NOTES
Assumptions:
- The Invoke-WebRequest cmdlet is available on the system where the script is being run.
- The specified JSON file exists and is readable by the PowerShell process running the script.
- The specified base URL is valid and the endpoint path (/LogAPI/api/logevent) is correct.

Error Handling:
- If the request succeeds (i.e. returns a status code of 200), the JSON response content is parsed and output to the console.
- If the request fails (i.e. returns a status code other than 200), an error message is output to the console.
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$BaseUrl,
    [Parameter(Mandatory=$true)]
    [string]$JsonFilePath
)

# Combine the base URL and the LogAPI endpoint
$Url = "$BaseUrl/LogAPI/api/logevent"

# Read the contents of the JSON file
$Json = Get-Content -Path $JsonFilePath -Raw

# Make the POST request using Invoke-WebRequest
$Result = Invoke-WebRequest -Uri $Url -Method Post -Body $Json -ContentType 'application/json'

# Parse the JSON response and output it to the console
try {
    $Response = ConvertFrom-Json $Result.Content
    Write-Output $Response
} catch {
    Write-Error "Failed to parse response as JSON: $_"
}

# Check for errors
if ($Result.StatusCode -ne 200) {
    Write-Error "Request failed with status code $($Result.StatusCode)"
}
