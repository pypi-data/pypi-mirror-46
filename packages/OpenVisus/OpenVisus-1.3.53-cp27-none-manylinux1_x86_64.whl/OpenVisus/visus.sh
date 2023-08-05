#!/bin/bash
this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHON_EXECUTABLE=/root/.pyenv/versions/2.7.15/bin/python
export PYTHON_PATH=${this_dir}:/root/OpenVisus.build/RelWithDebInfo/site-packages/OpenVisus:/root/.pyenv/versions/2.7.15/lib/python27.zip:/root/.pyenv/versions/2.7.15/lib/python2.7:/root/.pyenv/versions/2.7.15/lib/python2.7/plat-linux2:/root/.pyenv/versions/2.7.15/lib/python2.7/lib-tk:/root/.pyenv/versions/2.7.15/lib/python2.7/lib-old:/root/.pyenv/versions/2.7.15/lib/python2.7/lib-dynload:/root/.pyenv/versions/2.7.15/lib/python2.7/site-packages
export LD_LIBRARY_PATH=/root/.pyenv/versions/2.7.15/lib
${this_dir}/bin/visus $@
