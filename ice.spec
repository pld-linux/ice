
Summary:	Ice
Summary(pl.UTF-8):	Ice
Name:		Ice
Version:	3.4.0
Release:	1
License:	GPL and Custom (see ICE_LICENSE)
Group:		Applications
Source0:	http://www.zeroc.com/download/Ice/3.4/%{name}-%{version}.tar.gz
# Source0-md5:	998b10627ade020cb00f5beb73efc0e0
URL:		http://www.zeroc.com
Patch0:		%{name}-build.patch
BuildRequires:	db4.5-cxx-devel
BuildRequires:	mcpp-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ice.

%description -l pl.UTF-8
Ice.

%package devel
Summary:	Header files for Ice library
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotekiIce
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Ice library.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotekiIce.

%prep
%setup -q
%patch0 -p0

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/usr,%{_datadir},%{_datadir}/%{name}}

%{__make} install \
	prefix=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/bin $RPM_BUILD_ROOT/usr
mv $RPM_BUILD_ROOT/include $RPM_BUILD_ROOT/usr
mv $RPM_BUILD_ROOT/lib64 $RPM_BUILD_ROOT/usr
mv $RPM_BUILD_ROOT/slice $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ICE_LICENSE
%attr(755,root,root) %{_bindir}/dumpdb
%attr(755,root,root) %{_bindir}/glacier2router
%attr(755,root,root) %{_bindir}/icebox
%attr(755,root,root) %{_bindir}/iceboxadmin
%attr(755,root,root) %{_bindir}/iceca
%attr(755,root,root) %{_bindir}/icegridadmin
%attr(755,root,root) %{_bindir}/icegridnode
%attr(755,root,root) %{_bindir}/icegridregistry
%attr(755,root,root) %{_bindir}/icepatch2calc
%attr(755,root,root) %{_bindir}/icepatch2client
%attr(755,root,root) %{_bindir}/icepatch2server
%attr(755,root,root) %{_bindir}/icestormadmin
%attr(755,root,root) %{_bindir}/icestormmigrate
%attr(755,root,root) %{_bindir}/slice2cpp
%attr(755,root,root) %{_bindir}/slice2cs
%attr(755,root,root) %{_bindir}/slice2freeze
%attr(755,root,root) %{_bindir}/slice2freezej
%attr(755,root,root) %{_bindir}/slice2html
%attr(755,root,root) %{_bindir}/slice2java
%attr(755,root,root) %{_bindir}/slice2php
%attr(755,root,root) %{_bindir}/slice2py
%attr(755,root,root) %{_bindir}/slice2rb
%attr(755,root,root) %{_bindir}/transformdb
%attr(755,root,root) %{_libdir}/libFreeze.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libFreeze.so.34
%attr(755,root,root) %{_libdir}/libGlacier2.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libGlacier2.so.34
%attr(755,root,root) %{_libdir}/libIce.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIce.so.34
%attr(755,root,root) %{_libdir}/libIceBox.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceBox.so.34
%attr(755,root,root) %{_libdir}/libIceDB.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceDB.so.34
%attr(755,root,root) %{_libdir}/libIceGrid.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceGrid.so.34
%attr(755,root,root) %{_libdir}/libIceGridFreezeDB.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceGridFreezeDB.so.34
%attr(755,root,root) %{_libdir}/libIcePatch2.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIcePatch2.so.34
%attr(755,root,root) %{_libdir}/libIceSSL.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceSSL.so.34
%attr(755,root,root) %{_libdir}/libIceStorm.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceStorm.so.34
%attr(755,root,root) %{_libdir}/libIceStormFreezeDB.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceStormFreezeDB.so.34
%attr(755,root,root) %{_libdir}/libIceStormService.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceStormService.so.34
%attr(755,root,root) %{_libdir}/libIceUtil.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceUtil.so.34
%attr(755,root,root) %{_libdir}/libIceXML.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libIceXML.so.34
%attr(755,root,root) %{_libdir}/libSlice.so.3.4.0
%attr(755,root,root) %ghost %{_libdir}/libSlice.so.34
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libFreeze.so
%attr(755,root,root) %{_libdir}/libGlacier2.so
%attr(755,root,root) %{_libdir}/libIce.so
%attr(755,root,root) %{_libdir}/libIceBox.so
%attr(755,root,root) %{_libdir}/libIceDB.so
%attr(755,root,root) %{_libdir}/libIceGrid.so
%attr(755,root,root) %{_libdir}/libIceGridFreezeDB.so
%attr(755,root,root) %{_libdir}/libIcePatch2.so
%attr(755,root,root) %{_libdir}/libIceSSL.so
%attr(755,root,root) %{_libdir}/libIceStorm.so
%attr(755,root,root) %{_libdir}/libIceStormFreezeDB.so
%attr(755,root,root) %{_libdir}/libIceStormService.so
%attr(755,root,root) %{_libdir}/libIceUtil.so
%attr(755,root,root) %{_libdir}/libIceXML.so
%attr(755,root,root) %{_libdir}/libSlice.so
%{_includedir}/Freeze
%{_includedir}/Glacier2
%{_includedir}/Ice
%{_includedir}/IceBox
%{_includedir}/IceGrid
%{_includedir}/IcePatch2
%{_includedir}/IceSSL
%{_includedir}/IceStorm
%{_includedir}/IceUtil
%{_includedir}/IceXML
%{_includedir}/Slice
