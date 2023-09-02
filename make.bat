@ECHO OFF

for /f "usebackq" %%a in (`rye version`) do set VER=%%a

set CURRENT=%~dp0
set RELEASE=%CURRENT%release
set RELEASE_TEMP=%CURRENT%release_temp


cd /d %~dp0


del /Q /S %RELEASE%
del /Q /S %RELEASE_TEMP%
mkdir %RELEASE%
mkdir %RELEASE_TEMP%

rye run pyinstaller.exe src\bufap\cli\bufap-cli.spec --distpath %RELEASE_TEMP%
rye run pyinstaller.exe src\bufap\gui\bufap-gui.spec --distpath %RELEASE_TEMP%


COPY README.md %RELEASE_TEMP%

pushd %RELEASE_TEMP%
powershell compress-archive -Force * %RELEASE%\bufap-%VER%.zip
popd

git flow release finish %VER%
git push --tags

git switch main

rye build --clean
rye publish