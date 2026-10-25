' Starts Cutito without a black window, without needing to build the .exe.
' Requires start.bat to have been run at least once (it creates the Python environment).
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
here = fso.GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = here
py = here & "\.venv\Scripts\pythonw.exe"
If Not fso.FileExists(py) Then
    MsgBox "Run start.bat once first, so it installs everything that is needed.", 48, "Cutito"
Else
    sh.Run """" & py & """ """ & here & "\app.py""", 0, False
End If
