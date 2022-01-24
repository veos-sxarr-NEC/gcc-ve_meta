%global	pname gcc-ve
%global gcc_version 7.1.0
%global gcc_release 7

Name: %{pname}
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
Summary: Various compilers proted to VE (C, C++, Objective-C, Java, ...)

%global pkgdir	%{pname}-%{version}
%global gcc_target_platform ve-nec-linux-gnu
%global gcc_source gcc_source
%global gcc_meta gcc_meta
%global gcc_build build
%global prefix /opt/nec/ve
%global L_infodir share/info
%global infodir %{prefix}/%{L_infodir}
%global L_mandir share/man
%global mandir %{prefix}/%{L_mandir}
%global _sysconfdir /etc%{prefix}
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
Requires: libgcc-ve-static = %{version}-%{release}

%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%define __strip %{metadir}/wrap-strip
# %%define __os_install_post /usr/lib/rpm/brp-compress || :

%description
The gcc package contains the GNU Compiler Collection version 7.
You'll need this package in order to compile C code.
This package provides GCC ported to VE

%package -n libgcc-ve-static
Summary: GCC version 7 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc-ve-static
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
make %{?_smp_mflags} prefix=${RPM_BUILD_ROOT}%{prefix} install

cp %{metadir}/glibc-gcc.specs ${RPM_BUILD_ROOT}%{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/specs
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/gcc
cd ${RPM_BUILD_ROOT}%{prefix}/lib/gcc
ln -s %{gcc_target_platform}/%{gcc_version}/libgcc.a libgcc.a
cp %{sourcedir}/README* ${RPM_BUILD_DIR}/%{gcc_build}/
cp %{sourcedir}/COPYING* ${RPM_BUILD_DIR}/%{gcc_build}/

rm -fr ${RPM_BUILD_ROOT}%{infodir}/dir

###
### Workaround for search path of gcc
###
cd ${RPM_BUILD_ROOT}%{prefix}/%{gcc_target_platform}
mv include/c++ ../include
rm -fr include
mv lib/* ../lib
rm -fr lib
###

%clean
rm -fr ${RPM_BUILD_ROOT}

%pre
###
### Workaround for search path of gcc
###
if [ -d %{prefix}/ve-nec-linux/include ]; then
  rm -fr %{prefix}/ve-nec-linux/include
fi

if [ -d %{prefix}/ve-nec-linux/lib ]; then
  cd %{prefix}/ve-nec-linux/lib
  rm -fr audit gcc gconv *crt*.o lib* ld-*.so*
fi

if [ -d %{prefix}/%{gcc_target_platform} ]; then
  cd %{prefix}/%{gcc_target_platform}
  rm -fr include lib
fi
###

%files
%defattr(-,root,root)
%{prefix}/bin/c++
%{prefix}/bin/cpp
%{prefix}/bin/g++
%{prefix}/bin/gcc
%{prefix}/bin/gcc-ar
%{prefix}/bin/gcc-nm
%{prefix}/bin/gcc-ranlib
%{prefix}/bin/gcov
%{prefix}/bin/gcov-dump
%{prefix}/bin/gcov-tool
%{prefix}/bin/%{gcc_target_platform}-gcc-%{gcc_version}

%dir %{prefix}/include/c++
%{prefix}/include/c++/%{gcc_version}

%{prefix}/lib/libsupc++.la
%{prefix}/lib/libsupc++.a
%{prefix}/lib/libstdc++fs.la
%{prefix}/lib/libstdc++fs.a
%{prefix}/lib/libstdc++.la
%{prefix}/lib/libstdc++.a
%{prefix}/lib/libstdc++.a-gdb.py*
%{prefix}/lib/libssp.la
%{prefix}/lib/libssp_nonshared.la
%{prefix}/lib/libssp.a
%{prefix}/lib/libssp_nonshared.a
%{prefix}/lib/libgomp.spec
%{prefix}/lib/libgomp.la
%{prefix}/lib/libgomp.a
%{prefix}/lib/libatomic.la
%{prefix}/lib/libatomic.a

%dir %{prefix}/lib/gcc
%dir %{prefix}/lib/gcc/%{gcc_target_platform}
%dir %{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/specs

%{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed
%{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/install-tools
%{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin

%{prefix}/lib64/libcc1.so*
%{prefix}/lib64/libcc1.la
%{prefix}/lib64/libcc1.a

%{prefix}/libexec/gcc

%dir %{prefix}/%{gcc_target_platform}

%{prefix}/share/gcc-%{gcc_version}

%{infodir}/cpp.info
%{infodir}/cppinternals.info
%{infodir}/gcc.info
%{infodir}/gccinstall.info
%{infodir}/gccint.info
%{infodir}/libgomp.info

%{prefix}/share/locale/*/LC_MESSAGES/gcc.mo
%{prefix}/share/locale/*/LC_MESSAGES/cpplib.mo
%{prefix}/share/locale/*/LC_MESSAGES/libstdc++.mo

%{mandir}/man1/cpp.1
%{mandir}/man1/g++.1
%{mandir}/man1/gcc.1
%{mandir}/man1/gcov.1
%{mandir}/man1/gcov-dump.1
%{mandir}/man1/gcov-tool.1
%{mandir}/man7/fsf-funding.7
%{mandir}/man7/gfdl.7
%{mandir}/man7/gpl.7

%{_sysconfdir}/gcc

%doc README README.md COPYING COPYING3 COPYING3.LIB COPYING.LIB COPYING.RUNTIME

%files -n libgcc-ve-static
%{prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
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
