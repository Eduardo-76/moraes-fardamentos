#define MyAppName "Fardamento App"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Moraes Fardamentos"
#define MyAppExeName "FardamentoApp.exe"

[Setup]
AppId={{A7E4D5F2-8C31-4B7A-9D26-51F8C2A4E903}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={localappdata}\Programs\FardamentoApp
DefaultGroupName={#MyAppName}

OutputDir=release_installer
OutputBaseFilename=FardamentoApp_Setup

Compression=lzma
SolidCompression=yes

WizardStyle=modern

PrivilegesRequired=lowest

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DisableProgramGroupPage=yes

UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "dist\FardamentoApp\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs; Excludes: "data\*;storage\*"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent