; NSIS Script for Ghastly
; Written by Krishna Manaswi Digumarti and Sundara Tejaswi Digumarti

; ==================================================
; --- INCLUDES ---
!include "MUI2.nsh"


; ==================================================
; --- COMPILE TIME CONSTANTS ---
; all variables are global no matter where they are declared
!define APPLICATION_NAME "Ghastly"
!define DESCRIPTION "A pdf manipulation utility"
!define INSTALLSIZE 55000 ; [kb]

; These must be integers
!define VERSION_MAJOR 1
!define VERSION_MINOR 1

; These will be displayed by the "Click here for support information" link in "Add/Remove Programs"
; It is possible to use "mailto:" links in here to open the email client
!define HELPURL "http://..." # "Support Information" link
!define UPDATEURL "http://..." # "Product Updates" link
!define ABOUTURL "http://..." # "Publisher" link


; ==================================================
; --- GENERAL ---
Name ${APPLICATION_NAME}
Icon "icons\icon.ico"
OutFile "Ghastly-1.1-setup.exe" ; this is the name of the exe file that this script creates

; Properly display all languages (Installer will not work on Windows 95, 98 or ME!)
Unicode True

; Default installation folder
InstallDir "$PROGRAMFILES\${APPLICATION_NAME}"

; Allow install to root directory
AllowRootDirInstall true  

; Get installation folder from registry if available
InstallDirRegKey HKCU "Software\${APPLICATION_NAME}" ""

; Request application privileges for Windows Vista and higher
RequestExecutionLevel admin

; Show the installation details
ShowInstDetails show

; Show the uninstallation details
ShowUninstDetails show

; Branding. The text that appears at the bottom of the install window.
BrandingText " "


; ==================================================
; --- LANGUAGES ---
 !insertmacro MUI_LANGUAGE "English"


; ==================================================
; --- VERSION INFORMATION ---
; Output exe version information - shows up in the file properties
VIProductVersion "1.1.0.0"
VIFileVersion "1.1.0.0"
VIAddVersionKey "ProductName" ${APPLICATION_NAME}
VIAddVersionKey "LegalCopyright" "© Sundara Tejaswi Digumarti and Krishna Manaswi Digumarti"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" ${APPLICATION_NAME}


; ==================================================
; --- COMPILER FLAGS ---
; Use LZMA Compression algorithm, compression quality is better.
SetCompressor lzma
; regenerate install date each time
SetDateSave off 


; ==================================================
; --- INTERFACE SETTINGS ---
; MUI_*Macros at the beginning are defined in MUI2.nsh File, please check Modern UI 2 Description.

!define MUI_ICON "icons\icon.ico"                                   ; The icon file used by the installation package. 
!define MUI_UNICON "icons\icon.ico"                                 ; uninstall icon
!define MUI_HEADERIMAGE_BITMAP "icons\installer_header.bmp"         ; header image for installer page
!define MUI_HEADERIMAGE_UNBITMAP  "icons\installer_header.bmp"      ; header image for uninstaller page
!define MUI_WELCOMEFINISHPAGE_BITMAP "icons\installer_welcome.bmp"  ; image for start and finish pages
!define MUI_FINISHPAGE_NOAUTOCLOSE                                  ; Do not automatically jump to the finish page. Allow the user to check the install log
!define MUI_ABORTWARNING                                            ; Display a prompt if the user stops the installation mid way


; ==================================================
; --- INSTALLER PAGES ---
; These are displayed in the order that they are inserted
; !defines must come before the page

; Welcome page
; This function is called then the Next button is presed on the welcome screen
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE "OnPageWelcomeLeave"
!insertmacro MUI_PAGE_WELCOME

; Directory selection page
; This function is called when the Next button is pressed on the directory selection page
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE "OnPageDirectoryLeave"
!insertmacro MUI_PAGE_DIRECTORY

; Components page
!define MUI_COMPONENTSPAGE_NODESC ; no descriptions will be displayed for individual components
!insertmacro MUI_PAGE_COMPONENTS

; Install files page
!insertmacro MUI_PAGE_INSTFILES

; Finish page
!insertmacro MUI_PAGE_FINISH


; ==================================================
; --- USER DEFINED MACROS ---
!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin" ;Require admin rights on NT4+
        messageBox mb_iconstop "Administrator rights required!"
        setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
        quit
${EndIf}
!macroend


; ==================================================
; --- INSTALLER SECTIONS --- 
; The installation package must have at least one section (can also think of these as components).
; Named sections show up in the components page as a selectable list.
; Sections are executed in the instfiles page in the order in which they are defined.
; Commands written within sections are executed sequentially during installation.

Section "Ghastly - main program"
  SectionIn RO ; Read only, always installed

  ; Sets output directory
  SetOutPath "$INSTDIR"

  ; Files - To build the installer these files shouls be relative to this script
  /* 
  This command is special in that it defines both the files to be packaged and the files to be unpacked at installation time.
  The path defined here is the path to the files to be packaged. Since I am using pyinstaller, the files are in the dist folder.
  All files in a directory can also be specified as a single file.
  When installed, the file will be unpacked to SetOutPath.
  If File command defines several files all the files will be unpacked according to the directory structure they had before packing.
  Files added here should be removed by the uninstaller.
  */
  File /r "dist\main\*.*" 
                      
  ; Uninstaller - See function un.onInit and section "uninstall" for configuration
  writeUninstaller "$INSTDIR\uninstall_${APPLICATION_NAME}.exe"

  ; Registry information for add/remove programs
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "DisplayName" "${APPLICATION_NAME} - ${DESCRIPTION}"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "UninstallString" "$\"$INSTDIR\uninstall_${APPLICATION_NAME}.exe$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall_${APPLICATION_NAME}.exe$\" /S"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "InstallLocation" "$\"$INSTDIR$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "DisplayIcon" "$\"$INSTDIR\icons\icon.ico$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "Publisher" "$\"ST and KM Digumarti$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "HelpLink" "$\"${HELPURL}$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "URLUpdateInfo" "$\"${UPDATEURL}$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "URLInfoAbout" "$\"${ABOUTURL}$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "DisplayVersion" "${VERSION_MAJOR}.${VERSION_MINOR}"
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "VersionMajor" ${VERSION_MAJOR}
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "VersionMinor" ${VERSION_MINOR}
	
  ; There is no option for modifying or repairing the install
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "NoModify" 1
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "NoRepair" 1
	
  ; Set the INSTALLSIZE constant (!defined at the top of this script) so Add/Remove Programs can accurately report the size
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}" "EstimatedSize" ${INSTALLSIZE}

SectionEnd

Section "Start menu shortcut"
  ; Start menu
  createDirectory "$SMPROGRAMS\${APPLICATION_NAME}"
  createShortCut "$SMPROGRAMS\${APPLICATION_NAME}\${APPLICATION_NAME}.lnk" "$INSTDIR\main.exe" "" "$INSTDIR\icons\icon.ico"
  createShortCut "$SMPROGRAMS\${APPLICATION_NAME}\Uninstall-${APPLICATION_NAME}.lnk" "$INSTDIR\uninstall_${APPLICATION_NAME}.exe" "" "$INSTDIR\icons\icon.ico"
SectionEnd

Section "Desktop shortcut"
  ; Desktop shortcut
  createShortCut "$DESKTOP\${APPLICATION_NAME}.lnk" "$INSTDIR\main.exe" "" "$INSTDIR\icons\icon.ico"
SectionEnd

; ==================================================
; --- INSTALLER FUNCTIONS ---
; NSIS scripting convention is that functions must be written at the end of the script.
; The . at the beginning indicates a built-in call-back function that is executed at a specific time

; This function is executed when the package starts. 
Function .onInit
  setShellVarContext all
	!insertmacro VerifyUserIsAdmin
FunctionEnd

Function OnPageWelcomeLeave

FunctionEnd

Function OnPageDirectoryLeave

FunctionEnd


; ==================================================
; --- UNINSTALLER SECTIONS ---

section "uninstall"
 
	; Remove Start Menu launcher
	delete "$SMPROGRAMS\${APPLICATION_NAME}\${APPLICATION_NAME}.lnk"
  delete "$SMPROGRAMS\${APPLICATION_NAME}\Uninstall_${APPLICATION_NAME}.lnk"
	
  ; Try to remove the Start Menu folder - this will only happen if it is empty
	rmDir "$SMPROGRAMS\${APPLICATION_NAME}"
 
  ; remove desktop shortcut
  delete "$DESKTOP\${APPLICATION_NAME}.lnk"

	; Remove files
	delete $INSTDIR\main.exe
  delete $INSTDIR\main.exe.manifest
  delete $INSTDIR\*.pyd
  delete $INSTDIR\*.dll
  delete $INSTDIR\*.zip
  delete $INSTDIR\icons\*.*
  delete $INSTDIR\platforms\*.*
  delete $INSTDIR\PySide6\*.*
  delete $INSTDIR\shiboken6\*.*
  
	; Always delete uninstaller as the last action
	delete $INSTDIR\uninstall_${APPLICATION_NAME}.exe
 
	; Try to remove the install directory - this will only happen if it is empty
  rmDir $INSTDIR\icons
  rmDir $INSTDIR\platforms
  rmDir $INSTDIR\PySide6
  rmDir $INSTDIR\shiboken6
	rmDir $INSTDIR
 
	; Remove uninstaller information from the registry
	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPLICATION_NAME}"
sectionEnd


; ==================================================
; --- UNINSTALLER FUNCTIONS ---

; uninstaller function
Function un.onInit
	SetShellVarContext all
 
	; check if the user really wants to uninstall
	MessageBox MB_OKCANCEL "Permanantly remove ${APPLICATION_NAME}?" IDOK next
		Abort
	next:
	!insertmacro VerifyUserIsAdmin
FunctionEnd


; --- THE END ---