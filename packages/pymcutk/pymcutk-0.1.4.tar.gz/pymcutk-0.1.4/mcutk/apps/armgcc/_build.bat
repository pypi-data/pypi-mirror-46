@echo off
set ARMGCC_DIR=%~3

cd /d %1

REM clean projects
if exist CMakeFiles (
    rd /s /Q CMakeFiles
)
if exist %2 (
    rd /s /Q %2
)
del /s /Q /F Makefile cmake_install.cmake CMakeCache.txt

%4 -DCMAKE_TOOLCHAIN_FILE=%5 -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=%2 .

if not %errorlevel% == 0 (exit /b %errorlevel%)

%6 -C . -j4

exit /b %errorlevel%