@echo off
REM este script es lo que windows ejecutara automaticamente cada mañana
REM lo que hara es que ingresara la capeta del proyecto y correra el main.py igual que se hace a mano por terminal

cd /d "C:\Users\user\Desktop\data-engineering\Scraper-Trabajo"
python main.py >> log_ejecucion.txt 2>&1