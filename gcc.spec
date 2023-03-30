%global	pname gcc-ve3
%global gcc_version 7.1.0
%global gcc_release 9

Name: %{pname}
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
Summary: Various compilers proted to VE (C, C++, Objective-C, Java, ...)

%global gccdir /gcc
%global pkgdir	%{pname}-%{version}
%global gcc_target_platform ve-nec-linux-gnu
%global gcc_source gcc_source
%global gcc_meta gcc_meta
%global gcc_build build
%global program_prefix ve-
%global prefix /opt/nec/ve3
%global L_infodir share/info
%global infodir %{prefix}%{gccdir}/%{L_infodir}
%global L_mandir share/man
%global mandir %{prefix}%{gccdir}/%{L_mandir}
%global metadir ${RPM_BUILD_DIR}/%{gcc_meta}
%global sourcedir ${RPM_BUILD_DIR}/%{gcc_source}

# libgcc, libgfortran, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
Source0: gcc_meta-ve-%{version}.tar.bz2
Source1: gcc_source-ve-%{version}.tar.bz2
Vendor:	NEC Corporation
ExclusiveArch: x86_64
BuildArch: x86_64
BuildRequires: readline-devel >= 6.2-4
BuildRequires: ncurses-devel texinfo gettext flex bison
BuildRequires: expat-devel
BuildRequires: zlib-devel
BuildRequires: libstdc++
BuildRequires: texinfo-tex
BuildRequires: texlive-collection-latexrecommended
BuildRequires: info
BuildRequires: gzip
BuildRequires: veos-devel
%if 0%{?rhel} == 8
BuildRequires: python36-devel
%else
BuildRequires: python-devel
%endif
Requires: readline
Requires: zlib
Requires: expat
Requires: veos-libveptrace
Requires: libgcc-ve3-static = %{version}-%{release}

%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%define __strip %{metadir}/wrap-strip
# %%define __os_install_post /usr/lib/rpm/brp-compress || :

%description
The gcc package contains the GNU Compiler Collection version 7.
You'll need this package in order to compile C code.
This package provides GCC ported to VE

%package -n libgcc-ve3-static
Summary: GCC version 7 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc-ve3-static
This package contains GCC shared support library which is needed
e.g. for exception handling support.
This package provides GCC ported to VE

%prep
%setup -n %{gcc_meta} -c

%setup -T -n %{gcc_source} -c -a 1
patch -p1 -s < %{metadir}/source_gcc_configure.patch
tar -zxf %{metadir}/mpc-1.0.1.tar.gz
ln -s mpc-1.0.1 mpc

%setup -T -n %{gcc_build} -c

rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{prefix}

%build

%install
%{metadir}/config.sh -l gnu -i %{prefix}
make %{?_smp_mflags}
make %{?_smp_mflags} prefix=${RPM_BUILD_ROOT}%{prefix}%{gccdir} install

cp %{metadir}/glibc-gcc.specs ${RPM_BUILD_ROOT}%{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/specs
cd ${RPM_BUILD_ROOT}%{prefix}%{gccdir}/lib/gcc
ln -s %{gcc_target_platform}/%{gcc_version}/libgcc.a libgcc.a
mkdir -p ${RPM_BUILD_ROOT}%{prefix}/lib/gcc
cd ${RPM_BUILD_ROOT}%{prefix}/lib/gcc
ln -s ../../gcc/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a libgcc.a
cp %{sourcedir}/README* ${RPM_BUILD_DIR}/%{gcc_build}/
cp %{sourcedir}/COPYING* ${RPM_BUILD_DIR}/%{gcc_build}/

rm -fr ${RPM_BUILD_ROOT}%{infodir}/dir

%clean
rm -fr ${RPM_BUILD_ROOT}

%pre

%files
%defattr(-,root,root)
%{prefix}%{gccdir}/bin/%{program_prefix}c++
%{prefix}%{gccdir}/bin/%{program_prefix}cpp
%{prefix}%{gccdir}/bin/%{program_prefix}g++
%{prefix}%{gccdir}/bin/%{program_prefix}gcc
%{prefix}%{gccdir}/bin/%{program_prefix}gcc-ar
%{prefix}%{gccdir}/bin/%{program_prefix}gcc-nm
%{prefix}%{gccdir}/bin/%{program_prefix}gcc-ranlib
%{prefix}%{gccdir}/bin/%{program_prefix}gcov
%{prefix}%{gccdir}/bin/%{program_prefix}gcov-dump
%{prefix}%{gccdir}/bin/%{program_prefix}gcov-tool
%{prefix}%{gccdir}/bin/%{gcc_target_platform}-gcc-%{gcc_version}

%dir %{prefix}%{gccdir}/lib/gcc
%dir %{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}
%dir %{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/specs

%{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed
%{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/install-tools
%{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin

%{prefix}%{gccdir}/lib64/libcc1.so*
%{prefix}%{gccdir}/lib64/libcc1.la
%{prefix}%{gccdir}/lib64/libcc1.a

%{prefix}%{gccdir}/libexec/gcc

%{infodir}/cpp.info
%{infodir}/cppinternals.info
%{infodir}/gcc.info
%{infodir}/gccinstall.info
%{infodir}/gccint.info

%{prefix}%{gccdir}/share/locale/*/LC_MESSAGES/gcc.mo
%{prefix}%{gccdir}/share/locale/*/LC_MESSAGES/cpplib.mo

%{mandir}/man1/%{program_prefix}cpp.1
%{mandir}/man1/%{program_prefix}g++.1
%{mandir}/man1/%{program_prefix}gcc.1
%{mandir}/man1/%{program_prefix}gcov.1
%{mandir}/man1/%{program_prefix}gcov-dump.1
%{mandir}/man1/%{program_prefix}gcov-tool.1
%{mandir}/man7/fsf-funding.7
%{mandir}/man7/gfdl.7
%{mandir}/man7/gpl.7

%doc README README.md COPYING COPYING3 COPYING3.LIB COPYING.LIB COPYING.RUNTIME

%files -n libgcc-ve3-static
%{prefix}%{gccdir}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{prefix}%{gccdir}/lib/gcc/libgcc.a
%{prefix}/lib/gcc/libgcc.a

%doc README README.md COPYING COPYING3 COPYING3.LIB COPYING.LIB COPYING.RUNTIME

%changelog
* Fri Jul 27 2018 NEC 7.1.0-4
- Separated libgcc.a into libgcc package
- added dependency on libgcc package to gcc package

* Fri Jul 13 2018 NEC 7.1.0-3
- added a specs files for glibc and musl
- Modified to use the file in gcc_meta

* Thu Jun 14 2018 NEC 7.1.0-2
- workaround for search path of gcc

* Wed May 30 2018 NEC 7.1.0-1
- new package
