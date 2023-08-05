# NSIS script for creating the City Energy Analyst installer


; include the modern UI stuff
!include "MUI2.nsh"

# icon stuff
!define MUI_ICON "cea-icon.ico"


# download CEA conda env from here (FIXME: update to a more sane download URL)
# !define CEA_ENV_URL "https://polybox.ethz.ch/index.php/s/M8MYliTOGbbSCjH/download"
# !define CEA_ENV_FILENAME "cea.7z"
!define CEA_ENV_URL "https://github.com/architecture-building-systems/CityEnergyAnalyst/releases/download/v2.13/Dependencies.7z"
!define CEA_ENV_FILENAME "Dependencies.7z"
!define RELATIVE_GIT_PATH "Dependencies\cmder\vendor\git-for-windows\bin\git.exe"
!define CEA_REPO_URL "https://github.com/architecture-building-systems/CityEnergyAnalyst.git"

!define CEA_TITLE "City Energy Analyst"

# figure out the version based on cea\__init__.py
!system "get_version.exe"
!include "cea_version.txt"

Name "${CEA_TITLE} ${VER}"

!define MUI_FILE "savefile"
!define MUI_BRANDINGTEXT "${CEA_TITLE} ${VER}"
CRCCheck On


OutFile "Output\Setup_CityEnergyAnalyst_${VER}.exe"


;--------------------------------
;Folder selection page

InstallDir "$DOCUMENTS\CityEnergyAnalyst"

;Request application privileges for Windows Vista
RequestExecutionLevel user

;--------------------------------
;Interface Settings

!define MUI_ABORTWARNING

;--------------------------------
;Pages

!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Base Installation" Base_Installation_Section
    SectionIn RO  # this section is required
    SetOutPath "$INSTDIR"

    File "cea-icon.ico"

    # install cmder (incl. git and bash... woohoo!!)
    File /r "Dependencies"
    SetOutPath "$INSTDIR\Dependencies\cmder"
    Nsis7z::ExtractWithDetails "cmder.7z" "Installing CEA Console %s..."
    Delete "cmder.7z"
    SetOutPath "$INSTDIR"

    # make sure cmder can access our python (and the cea command)
    DetailPrint "Setting up CEA Console"
    CreateDirectory $INSTDIR\Dependencies\cmder\config\profile.d
    FileOpen $0 "$INSTDIR\Dependencies\cmder\config\profile.d\cea_path.bat" w
    FileWrite $0 "SET PATH=$INSTDIR\Dependencies\Python;$INSTDIR\Dependencies\Python\Scripts;$INSTDIR\Dependencies\Daysim;%PATH%"
    FileWrite $0 "$\r$\n" ; we write a new line
    FileWrite $0 "SET PYTHONHOME=$INSTDIR\Dependencies\Python"
    FileWrite $0 "$\r$\n" ; we write a new line
    FileWrite $0 "SET RAYPATH=$INSTDIR\Dependencies\Daysim"
    FileWrite $0 "$\r$\n" ; we write a new line
    FileWrite $0 "ALIAS find=$INSTDIR\Dependencies\cmder\vendor\git-for-windows\usr\bin\find.exe $*"
    FileClose $0


    # create a shortcut in the $INSTDIR for launching the CEA console
    CreateShortcut "$INSTDIR\CEA Console.lnk" "$INSTDIR\Dependencies\cmder\cmder.exe" "/single" \
        "$INSTDIR\cea-icon.ico" 0 SW_SHOWNORMAL \
        CONTROL|SHIFT|F10 "Launch the CEA Console"

    # create a shortcut in the $INSTDIR for launching the CEA dashboard
    CreateShortcut "$INSTDIR\CEA Dashboard.lnk" "$INSTDIR\Dependencies\Python\python.exe" "-m cea.interfaces.cli.cli dashboard" \
        "$INSTDIR\cea-icon.ico" 0 SW_SHOWMINIMIZED "" "Launch the CEA Dashboard"

    CreateShortcut "$INSTDIR\cea.config.lnk" "$WINDIR\notepad.exe" "$PROFILE\cea.config" \
        "$INSTDIR\cea-icon.ico" 0 SW_SHOWNORMAL "" "Open CEA Configuration file"


    ;Download the CityEnergyAnalyst conda environment
    DetailPrint "Downloading ${CEA_ENV_FILENAME}"
    inetc::get ${CEA_ENV_URL} ${CEA_ENV_FILENAME}
    Pop $R0 ;Get the return value
    StrCmp $R0 "OK" download_ok
        MessageBox MB_OK "Download failed: $R0"
        Quit
    download_ok:
        # get on with life...

    # unzip python environment to ${INSTDIR}\Dependencies
    DetailPrint "Extracting ${CEA_ENV_FILENAME}"
    Nsis7z::ExtractWithDetails ${CEA_ENV_FILENAME} "Installing Python %s..."
    Delete ${CEA_ENV_FILENAME}

    nsExec::ExecToLog '"$INSTDIR\Dependencies\Python\Scripts\pip.exe" install -U --no-cache cityenergyanalyst==${VER}'

    # create cea.config file in the %userprofile% directory by calling `cea --help` and set daysim paths
    nsExec::ExecToLog '"$INSTDIR\Dependencies\Python\Scripts\cea.exe" --help'
    WriteINIStr "$PROFILE\cea.config" radiation-daysim daysim-bin-directory "$INSTDIR\Dependencies\Daysim"

    ;Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

Section "Create Start menu shortcuts" Create_Start_Menu_Shortcuts_Section

    # create shortcuts in the start menu for launching the CEA console
    CreateDirectory '$SMPROGRAMS\${CEA_TITLE}'
    CreateShortCut '$SMPROGRAMS\${CEA_TITLE}\CEA Console.lnk' '$INSTDIR\Dependencies\cmder\cmder.exe' '/single' \
        "$INSTDIR\cea-icon.ico" 0 SW_SHOWNORMAL CONTROL|SHIFT|F10 "Launch the CEA Console"

    CreateShortcut "$SMPROGRAMS\${CEA_TITLE}\CEA Dashboard.lnk" "$INSTDIR\Dependencies\Python\python.exe" "-m cea.interfaces.cli.cli dashboard" \
        "$INSTDIR\cea-icon.ico" 0 SW_SHOWMINIMIZED "" "Launch the CEA Dashboard"

    CreateShortcut "$SMPROGRAMS\${CEA_TITLE}\cea.config.lnk" "$WINDIR\notepad.exe" "$PROFILE\cea.config" \
        "$INSTDIR\cea-icon.ico" 0 SW_SHOWNORMAL "" "Open CEA Configuration file"

SectionEnd

Section /o "Developer version" Clone_Repository_Section

    DetailPrint "Cloning GitHub Repository ${CEA_REPO_URL}"
    nsExec::ExecToLog '"$INSTDIR\${RELATIVE_GIT_PATH}" clone ${CEA_REPO_URL}'
    DetailPrint "Binding CEA to repository"
    nsExec::ExecToLog '"$INSTDIR\Dependencies\Python\Scripts\pip.exe" install -e "$INSTDIR\CityEnergyAnalyst"'

SectionEnd

;--------------------------------
;Descriptions

;Language strings
;  LangString DESC_SecDummy ${LANG_ENGLISH} "A test section."

  ;Assign language strings to sections
;  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
;    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
;  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\Modern UI Test"

SectionEnd