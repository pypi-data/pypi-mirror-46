set this_dir=%~dp0
set PYTHON_EXECUTABLE=C:\Python36-x64\python.exe
set PATH=%this_dir%\bin;%PYTHON_EXECUTABLE%\..;%PATH%
if EXIST %this_dir%\bin\Qt (
   echo "Using internal Qt5" 
   set Qt5_DIR=%this_dir%\bin\Qt
) else (
   echo "Using external PyQt5" 
   for /f "usebackq tokens=*" %%G in (`%PYTHON_EXECUTABLE% -c "import os,PyQt5; print(os.path.dirname(PyQt5.__file__))"`) do set Qt5_DIR=%%G\Qt
)
set QT_PLUGIN_PATH=%Qt5_DIR%\plugins
cd %this_dir%
%this_dir%\bin/visusviewer.exe %*
