$path = "\pmk_nal_3"
$mergedData = Get-ChildItem $path -Filter "*.csv" | ForEach-Object{
    $file = $_
    # Get the file data
    Get-Content $file.FullName | 
        # Skip the filename
        Select-Object -Skip 1 |
        # Now we can get CSV object in the same way that Import-CSV would generate 
        ConvertFrom-Csv | ForEach-Object{
            # Add the current filename as a column
            $_ | Add-Member -MemberType NoteProperty -Name "fileName" -Value $file.Name -PassThru
        }
# Convert back into raw, quoted data
} | ConvertTo-Csv -NoTypeInformation

# Prefix the header before the compiled data
"merged.csv",$mergedData | Set-Content "$path\merged.csv"