#define MyAppName "MineBlock 2D"
#define MyAppVersion "1.5.1"
#define MyAppPublisher "MineBlock 2D Dev Team"
#define MyAppURL "http://mineblock2d.ml/"
#define MyAppExeName "MineBlock 2D.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{D6E78475-C042-4B4C-979F-24728B99D48C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={#MyAppName} V{#MyAppVersion}
DefaultGroupName={#MyAppName}
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=commandline
OutputBaseFilename={#MyAppName} V{#MyAppVersion} Extractor
Compression=lzma
SolidCompression=yes
WizardStyle=modern
Uninstallable=no
SetupIconFile="..\icon.ico"

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: ".\dist\MineBlock 2D.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\dist\Arial Black.ttf"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\dist\Default_skin.png"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\dist\MineBlock 2D.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\dist\options.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\dist\Readme.html"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\dist\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\dist\Texture Packs\*"; DestDir: "{app}\Texture Packs"; Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
Name: "{app}\Worlds"
Name: "{app}\Screenshots"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

