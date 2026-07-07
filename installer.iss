[Setup]
AppName=Fabrik Frontend
AppVersion=0.1.0
DefaultDirName={autopf}\FabrikFrontend
OutputBaseFilename=fabrik-frontend-setup-0.1.0
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\fabrik-frontend\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Fabrik Frontend"; Filename: "{app}\fabrik-frontend.exe"
Name: "{commondesktop}\Fabrik Frontend"; Filename: "{app}\fabrik-frontend.exe"