; NSIS Script for Ghastly
; Written by Krishna Manaswi Digumarti and Sundara Tejaswi Digumarti

; ==================================================
; --- INCLUDES ---
!include "MUI2.nsh"


; ==================================================
; --- GENERAL ---
Name "Ghastly"
Icon "icon.ico"
OutFile "Ghastly.exe"

; Properly display all languages (Installer will not work on Windows 95, 98 or ME!)
Unicode True

; Default installation folder
InstallDir "$PROGRAMFILES\Ghastly"

; Allow install to root directory
AllowRootDirInstall true  

; Get installation folder from registry if available
InstallDirRegKey HKCU "Software\Ghastly" ""

; Request application privileges for Windows Vista
RequestExecutionLevel user

; Show the details by default. Installation details are displayed by default, and text messages output during installation are displayed.
ShowInstDetails show


; ==================================================
; --- COMPILER FLAGS ---
; Use LZMA Compression algorithm, compression quality is better.
SetCompressor lzma


; ==================================================
; --- INTERFACE SETTINGS ---
; MUI_*Macros at the beginning are defined in MUI2.nsh File, please check Modern UI 2 Description.

; The icon file used by the installation package. 
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\nsis3-install-alt.ico"

; uninstall icon
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\nsis3-uninstall.ico"

; Do not automatically jump to the finish page. Allow the user to check the install log
!define MUI_FINISHPAGE_NOAUTOCLOSE

; Display a prompt if the user stops the installation mid way
!define MUI_ABORTWARNING


; ==================================================
; --- INSTALLER PAGES ---
; These are displayed in the order that they are inserted

; Welcome page
; This function is called then the Next button is presed on the welcome screen
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE "OnPageWelcomeLeave"
!insertmacro MUI_PAGE_WELCOME

; Directory selection page
; This function is called when the Next button is pressed on the directory selection page
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE "OnPageDirectoryLeave"
!insertmacro MUI_PAGE_DIRECTORY

; Install files page
!insertmacro MUI_PAGE_INSTFILES

; Finish page
!insertmacro MUI_PAGE_FINISH


; ==================================================
; --- VERSION INFORMATION ---
; Output exe version information
VIProductVersion "1.1.0.0"
VIFileVersion "1.1.0.0"


; ==================================================
; --- LANGUAGES ---
 !insertmacro MUI_LANGUAGE "English"


; ==================================================
; --- INSTALLER SECTIONS ---
; Define the components of the installation process. 
; The installation package must have at least one component.
; If you have multiple components, you need to define multiple.
; Components can define component names and perform installation priorities.
; Commands written in components are executed sequentially during installation.

Section "Install"

  ; Sets output directory
  SetOutPath "$INSTDIR"

  ; Files - To build the installer these files shouls be relative to this script
  /* 
  This command is special in that it defines both the files to be packaged and the files to be unpacked at installation time.
  The path defined here is the path to the files to be packaged.
  All files in a directory can also be specified as a single file.
  When installed, the file will be unpacked to SetOutPath.
  If File command defines several files all the files will be unpacked according to the directory structure they had before packing.
  Files added here should be removed by the uninstaller.
  */
  File /r "Files\*.*" 
                      

  ; Uninstaller - See function un.onInit and section "uninstall" for configuration
  writeUninstaller "$INSTDIR\uninstall.exe"





SectionEnd


; ==================================================
; --- INSTALLER FUNCTIONS ---.
; NSIS scripting convention is that functions must be written at the end of the script.
; The . at the beginning indicates a built-in call-back function that is executed at a specific time

; This function is executed when the package starts. 
Function ".onInit"

FunctionEnd

Function "OnPageWelcomeLeave"

FunctionEnd

Function "OnPageDirectoryLeave"

FunctionEnd

; --- THE END ---