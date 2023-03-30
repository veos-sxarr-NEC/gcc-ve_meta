#!/bin/bash
# Target library change script.
#   Copyright (C) 2018-2021 NEC Corporation

# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <https://www.gnu.org/licenses/>.

set -x

SOURCE_PATH=../gcc_source

INSTALLBASE=/usr/local/ve/gcc
BINUTILS=/opt/nec/ve/bin
LIBC_TYPE=musl

while getopts "s:l:i:" OPT; do
    case $OPT in
        s)
	    SOURCE_PATH="$OPTARG";;
        l)
	    LIBC_TYPE="$OPTARG";;
        i)
	    INSTALLBASE="$OPTARG";;
    esac
done

if [ "$LIBC_TYPE" = "musl" ]; then
    LIBC_PATH=/opt/nec/ve/musl
    TARGET=ve-nec-linux-musl
elif [ "$LIBC_TYPE" = "gnu" ]; then
    LIBC_PATH=/opt/nec/ve3
    TARGET=ve-nec-linux-gnu
fi

date "+%Y%m%d" > $SOURCE_PATH/gcc/DATESTAMP
echo "experimental" > $SOURCE_PATH/gcc/DEV-PHASE
export PATH=/bin:/usr/bin

AS_FOR_TARGET=$BINUTILS/nas \
 LD_FOR_TARGET=$BINUTILS/nld \
 AR_FOR_TARGET=$BINUTILS/nar \
 NM_FOR_TARGET=$BINUTILS/nnm \
 STRIP_FOR_TARGET=$BINUTILS/nstrip \
 RANLIB_FOR_TARGET=$BINUTILS/nranlib \
 OBJDUMP_FOR_TARGET=$BINUTILS/nobjdump \
 READELF_FOR_TARGET=$BINUTILS/nreadelf \
 $SOURCE_PATH/configure \
 --build=i386-unknown-linux \
 --target=$TARGET \
 --prefix=$INSTALLBASE \
 --enable-languages=c,c++ \
 --enable-libstdc++-v3 \
 --disable-shared \
 --enable-static \
 --enable-sjlj-exceptions \
 --disable-libunwind-exceptions \
 --enable-tls \
 --with-as=$BINUTILS/nas \
 --with-ld=$BINUTILS/nld \
 --program-prefix="ve-" \
                --disable-libgloss \
                --disable-newlib \
                --disable-libgomp \
                --disable-libcilkrts \
                --disable-liboffloadmic \
                --disable-libhsail-rt \
                --disable-libatomic \
                --disable-libitm \
                --disable-libstdc++-v3 \
                --disable-libsanitizer \
                --disable-libvtv \
                --disable-libmpx \
                --disable-libssp \
                --disable-libquadmath \
                --disable-libgfortran \
                --disable-libffi \
                --disable-libobjc \
                --disable-libada \
                --disable-libgo

