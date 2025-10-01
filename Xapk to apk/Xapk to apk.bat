@echo off
echo === XAPK to APK Extractor ===
echo.

:: Python yoksa uyarı ver
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python.
    pause
    exit /b
)

:: Tüm .xapk dosyalarını sırayla işle
for %%f in (*.xapk) do (
    echo 🔄 Extracting %%f ...
    python xapk2toapk.py "%%f"
    echo.
)

echo ✅ All done!
pause
