' This script runs the batch file to start the application without showing a terminal window

Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")
strCurrentDirectory = objFSO.GetParentFolderName(WScript.ScriptFullName)
strBatchFilePath = objFSO.BuildPath(strCurrentDirectory, "run_app.bat")
objShell.Run Chr(34) & strBatchFilePath & Chr(34), 0
Set objFSO = Nothing
Set objShell = Nothing
