@echo off
chcp 65001 >nul
echo ========================================================
echo   ROBO BUSCADOR DE OFERTAS - CASA PRATICA E SMART
echo ========================================================
python "%~dp0robo_ofertas.py"
echo.
echo Catalogo atualizado com sucesso no arquivo produtos.js!
pause
