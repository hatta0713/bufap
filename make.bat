@ECHO OFF

set VER=%1

IF "a%VER%"=="a" (
    ECHO タグが指定されていません
    exit /b
)

IF not "a%VER%"=="adev" (
    git tag %VER%
    git push --tags
)

cd /d %~dp0
pyinstaller.exe bufap-cli.spec --distpath .

powershell compress-archive -Force bufap-cli.exe,bufap-getall.bat bufap-%VER%.zip

move /Y bufap-%VER%.zip dist
