set this_dir=%~dp0
set PYTHON_EXECUTABLE=C:\Python36-x64\python.exe
set PATH=%this_dir%\bin;%PYTHON_EXECUTABLE%\..;%PATH%
%this_dir%\bin/visus.exe %*
