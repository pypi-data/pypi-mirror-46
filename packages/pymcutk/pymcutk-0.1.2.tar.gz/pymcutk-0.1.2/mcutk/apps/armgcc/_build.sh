#!/bin/sh
cd $1
rm -rf CMakeFiles $2
rm -rf Makefile cmake_install.cmake CMakeCache.txt
export ARMGCC_DIR=$3
"$4" -DCMAKE_TOOLCHAIN_FILE=$5 -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=$2
if [ $? != 0 ];then
exit $?
fi
"$6" -C . -j4
exit $?
