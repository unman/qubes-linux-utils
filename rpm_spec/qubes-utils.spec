%define version %(cat version)
%if 0%{?qubes_builder}
%define _builddir %(pwd)
%endif

%{!?python_sitepath: %define python_sitepath %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

Name:		qubes-utils
Version:	%{version}
Release:	1%{?dist}
Summary:	Common Linux files for Qubes Dom0 and VM

Group:		Qubes
License:	GPL
URL:		http://www.qubes-os.org

Requires:	udev
Requires:	%{name}-libs
Requires:	ImageMagick
Requires:	pycairo
BuildRequires:  qubes-libvchan-devel
BuildRequires:  python-setuptools
# for meminfo-writer
BuildRequires:  xen-devel

%description
Common Linux files for Qubes Dom0 and VM

%package devel
Summary:	Development headers for qubes-utils
Release:	1%{?dist}
Requires:	%{name}-libs

%description devel
Development header and files for qubes-utils

%package libs
Summary: Qubes utils libraries
Release:	1%{?dist}

%description libs
Libraries for qubes-utils

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D


%build
make all

%install
make install DESTDIR=%{buildroot}

%post
# dom0
/bin/systemctl enable qubes-meminfo-writer-dom0.service > /dev/null 2>&1
# VM
/bin/systemctl enable qubes-meminfo-writer.service > /dev/null 2>&1

%postun
if [ $1 -eq 0 ]; then
    /bin/systemctl disable qubes-meminfo-writer.service > /dev/null 2>&1
    /bin/systemctl disable qubes-meminfo-writer.service > /dev/null 2>&1
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/lib/udev/rules.d/99-qubes-*.rules
/usr/lib/qubes/udev-*
%{_sbindir}/meminfo-writer
%{_unitdir}/qubes-meminfo-writer.service
%{_unitdir}/qubes-meminfo-writer-dom0.service
#%{python_sitearch}/qubes/__init__.py
#%{python_sitearch}/qubes/__init__.pyc
#%{python_sitearch}/qubes/__init__.pyo
%{python_sitepath}/qubesimgconverter/__init__.py*
%{python_sitepath}/qubesimgconverter/imggen.py*
%{python_sitepath}/qubesimgconverter/test.py*
%{python_sitepath}/qubesimgconverter-%{version}-py?.?.egg-info/*

%files libs
%{_libdir}/libqrexec-utils.so.2
%{_libdir}/libqubes-rpc-filecopy.so.2

%files devel
%defattr(-,root,root,-)
/usr/include/libqrexec-utils.h
/usr/include/libqubes-rpc-filecopy.h
/usr/include/qrexec.h
%{_libdir}/libqrexec-utils.so
%{_libdir}/libqubes-rpc-filecopy.so

%changelog

