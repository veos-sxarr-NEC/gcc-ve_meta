#!/usr/bin/bash
# GCC package build script.
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

GCC_VER=7.1.0
GCC_SDIR=${PWD}
RPMBUILD_TOP=~/rpmbuild

while getopts "s:t:" OPT; do
    case $OPT in
        s)
	    GCC_SDIR="$OPTARG";;
        t)
	    RPMBUILD_TOP="$OPTARG";;
    esac
done

META_SDIR=${GCC_SDIR}/gcc_meta
SOURCE_SDIR=${GCC_SDIR}/gcc_source
SPEC=${META_SDIR}/gcc.spec
META_TAR=gcc_meta-ve-${GCC_VER}.tar.bz2
SOURCE_TAR=gcc_source-ve-${GCC_VER}.tar.bz2
DOCDIR=/opt/nec/ve3/share/doc

if [ ! -d ${META_SDIR} ];then
	echo ${META_SDIR}" meta dir is not found" 
	exit 1
fi

if [ ! -d ${SOURCE_SDIR} ];then
	echo ${SOURCE_SDIR}" source dir is not found" 
	exit 1
fi

mkdir -p ${RPMBUILD_TOP}/{BUILD,SOURCES,SPECS,SRPMS,RPMS}

cd ${SOURCE_SDIR}
git archive --worktree-attributes --format=tar HEAD | bzip2 > ${RPMBUILD_TOP}/SOURCES/${SOURCE_TAR}

cd ${META_SDIR}
git archive --worktree-attributes --format=tar HEAD | bzip2 > ${RPMBUILD_TOP}/SOURCES/${META_TAR}

cp -f ${SPEC} ${RPMBUILD_TOP}/SPECS

export QA_SKIP_BUILD_ROOT=1
rpmbuild -D "_topdir ${RPMBUILD_TOP}" -D "_defaultdocdir ${DOCDIR}" -ba ${RPMBUILD_TOP}/SPECS/gcc.spec

