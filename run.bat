@echo off
chcp 65001 > nul
title Made by PhuogWin & PhongVeChai

:: Kiểm tra Python
C:\Users\namphong\AppData\Local\Programs\Python\Python311\python.exe --version > nul 2>&1
if errorlevel 1 (
    echo [!] Không tìm thấy Python. Vui lòng cài đặt Python!
    echo.
    pause
    exit
)

:: Kiểm tra file main.py
if not exist "main.py" (
    echo [!] Không tìm thấy file main.py!
    echo.
    pause
    exit
)

echo [*] Đang khởi chạy chương trình...
echo [*] Nhấn F8 để chụp ảnh và lấy đáp án
echo [*] Đóng cửa sổ chính để thoát
echo.
echo ═══════════════════════════════════════════════════════════
echo.

C:\Users\namphong\AppData\Local\Programs\Python\Python311\python.exe main.py

echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo [!] Chương trình đã dừng.
echo [*] Nhấn phím bất kỳ để thoát...
pause > nul