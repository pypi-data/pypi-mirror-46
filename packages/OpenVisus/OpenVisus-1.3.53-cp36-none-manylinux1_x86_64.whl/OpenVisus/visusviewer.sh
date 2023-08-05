#!/bin/bash
this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHON_EXECUTABLE=/root/.pyenv/versions/3.6.1/bin/python
export PYTHON_PATH=${this_dir}:/root/OpenVisus.build/RelWithDebInfo/site-packages/OpenVisus:/root/.pyenv/versions/3.6.1/lib/python36.zip:/root/.pyenv/versions/3.6.1/lib/python3.6:/root/.pyenv/versions/3.6.1/lib/python3.6/lib-dynload:/root/.pyenv/versions/3.6.1/lib/python3.6/site-packages
export LD_LIBRARY_PATH=/root/.pyenv/versions/3.6.1/lib
if [ -d ${this_dir}/bin/Qt ]; then 
   echo "Using internal Qt5" 
   export Qt5_DIR=${this_dir}/bin/Qt
else
   echo "Using external PyQt5" 
   export Qt5_DIR=$(${PYTHON_EXECUTABLE} -c "import os,PyQt5; print(os.path.dirname(PyQt5.__file__))")/Qt 
fi
export QT_PLUGIN_PATH=${Qt5_DIR}/plugins
cd ${this_dir}
${this_dir}/bin/visusviewer $@
