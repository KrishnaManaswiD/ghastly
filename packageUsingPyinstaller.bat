pyinstaller --noconfirm --log-level=WARN ^
    --onedir --noconsole ^
    --add-data icons\icon.ico;icons ^
    --add-data icons\icon.png;icons ^
    --add-data icons\icon_about.png;icons ^
    --add-data icons\icon_config.png;icons ^
    --add-data icons\icon_help.png;icons ^
    --add-data icons\installer_header.bmp;icons ^
    --add-data icons\installer_welcome.bmp;icons ^
    --icon=icons\icon.ico ^
    ghastly.py