# TODO
# - finish (pldize) -servers package
#
# Conditional build:
%bcond_without	gui		# IceGrid GUI
%bcond_without	dotnet		# .NET bindings
%bcond_with	java		# Java bindings (build requires X11 DISPLAY)
%bcond_with	php		# PHP bindings
%bcond_with	default_php	# build for default PHP
%bcond_without	python		# Python bindings
%bcond_without	ruby		# Ruby bindings

%if %{without java}
%undefine	with_gui
%endif

%ifarch x32
%undefine	with_dotnet
%endif

%if %{without default_php}
%if "%{?php_suffix}" == ""
%define		php_suffix	55
%endif
%endif
%define		php_name	php%{?php_suffix}

Summary:	The Ice base runtime and services
Summary(pl.UTF-8):	Podstawowy pakiet uruchomieniowy oraz usługowy Ice
Name:		ice
Version:	3.6.3
Release:	6
License:	GPL v2 with exceptions (see ICE_LICENSE)
Group:		Applications
#Source0Download: https://github.com/zeroc-ice/ice/releases
Source0:	https://github.com/zeroc-ice/ice/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	88bf025890cdd8d1193a7155dc539671
# Extracted from http://zeroc.com/download/Ice/3.6/rpm/el7/SRPMS/ice-3.6.3-1.el7.src.rpm
Source1:	Ice-rpmbuild-%{version}.tar.gz
# Source1-md5:	38536c26981a5cdc9b57723bc28aea44
Source3:	%{name}gridgui
Source4:	IceGridAdmin.desktop
Patch0:		no-arch-opts.patch
Patch1:		csharp-build.patch
Patch2:		%{name}-db.patch
Patch3:		%{name}-php7.patch
URL:		http://www.zeroc.com/
BuildRequires:	bzip2-devel
BuildRequires:	db-cxx-devel
BuildRequires:	expat-devel
BuildRequires:	mcpp-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.665
%if %{with gui}
BuildRequires:	ImageMagick
BuildRequires:	ImageMagick-coder-png
%endif
%if %{with dotnet}
BuildRequires:	mono-csharp
%endif
%if %{with java}
BuildRequires:	ant
BuildRequires:	db-java-devel
BuildRequires:	java-jgoodies-common
BuildRequires:	java-jgoodies-forms
BuildRequires:	java-jgoodies-looks
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
%endif
%if %{with php}
BuildRequires:	%{php_name}-devel >= 3:5.0.0
%endif
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
%endif
%if %{with ruby}
BuildRequires:	rpm-rubyprov
BuildRequires:	ruby >= 1:1.8.6
BuildRequires:	ruby-devel
%endif
# Ice doesn't officially support ppc64 at all; sparc64 doesn't have mono
ExcludeArch:	ppc64 sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Some file suffixes we need to grab the right stuff for the file lists
%define		soversion	36

%description
Ice is a modern alternative to object middleware such as CORBA or
COM/DCOM/COM+. It is easy to learn, yet provides a powerful network
infrastructure for demanding technical applications. It features an
object-oriented specification language, easy to use C++, C#, Java,
Python, Ruby, PHP, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic
transport plug-ins, TCP/IP and UDP/IP support, SSL-based security, a
firewall solution, and much more.

%description -l pl.UTF-8
Ice to współczesna alternatywa dla pośredniej warstwy obiektowej,
takiej jak CORBA lub COM/DCOM/COM+. Jest łatwy do nauczenia, a daje
potężną infrastrukturę sieciową dla wymagających aplikacji
technicznych. Ma zorientowany obiektowo język specyfikacji, łatwe do
nauki odwzorowania w C++, C#, Javie, Pythonie, Rubym, PHP i Visual
Basicu, bardzo wydajny protokół, asynchroniczne wywoływanie i
ekspediowanie metod, dynamiczne wtyczki transportowe, obsługę TCP/IP
oraz UDP/IP, szyfrowanie oparte na SSL, wbudowany firewall.

%package devel
Summary:	Tools for developing Ice applications in C++
Summary(pl.UTF-8):	Narzędzia do tworzenia aplikacji Ice w C++
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Tools for developing Ice applications in C++.

%description devel -l pl.UTF-8
Narzędzia do tworzenia aplikacji Ice w C++.

%package servers
Summary:	Ice services to run through /etc/rc.d/init.d
Summary(pl.UTF-8):	Usługi Ice do uruchamiania z poziomu /etc/rc.d/init.d
Group:		Development/Tools
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description servers
Ice services to run through /etc/rc.d/init.d.

%description servers -l pl.UTF-8
Usługi Ice do uruchamiania z poziomu /etc/rc.d/init.d.

%package -n icegrid-gui
Summary:	IceGrid Admin Tool
Summary(pl.UTF-8):	Narzędzie administracyjne IceGrid
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	java-%{name} = %{version}-%{release}
Requires:	java-jgoodies-forms
Requires:	java-jgoodies-looks
Requires:	jpackage-utils

%description -n icegrid-gui
Graphical administration tool for IceGrid.

%description -n icegrid-gui -l pl.UTF-8
Graficzne narzędzie administracyjne do IceGrida.

%package -n java-%{name}
Summary:	The Ice runtime for Java
Summary(pl.UTF-8):	Pakiet uruchomieniowy Ice dla Javy
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}
Requires:	db-java
Requires:	jpackage-utils

%description -n java-%{name}
The Ice runtime for Java.

%description -n java-%{name} -l pl.UTF-8
Pakiet uruchomieniowy Ice dla Javy.

%package -n csharp-%{name}
Summary:	The Ice runtime for C#
Summary(pl.UTF-8):	Pakiet uruchomieniowy Ice dla C#
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mono >= 1.2.2

%description -n csharp-%{name}
The Ice runtime for C#.

%description -n csharp-%{name} -l pl.UTF-8
Pakiet uruchomieniowy Ice dla C#.

%package -n ruby-%{name}
Summary:	The Ice runtime for Ruby applications
Summary(pl.UTF-8):	Pakiet uruchomieniowy Ice dla aplikacji w języku Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n ruby-%{name}
The Ice runtime for Ruby applications.

%description -n ruby-%{name} -l pl.UTF-8
Pakiet uruchomieniowy Ice dla aplikacji w języku Ruby.

%package -n python-%{name}
Summary:	The Ice runtime for Python applications
Summary(pl.UTF-8):	Pakiet uruchomieniowy Ice dla aplikacji w Pythonie
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python >= 1:2.3.4

%description -n python-%{name}
The Ice runtime for Python applications.

%description -n python-%{name} -l pl.UTF-8
Pakiet uruchomieniowy Ice dla aplikacji w Pythonie.

%package -n %{php_name}-%{name}
Summary:	The Ice runtime for PHP applications
Summary(pl.UTF-8):	Pakiet uruchomieniowy Ice dla aplikacji w PHP
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description -n %{php_name}-%{name}
The Ice runtime for PHP applications.

%description -n %{php_name}-%{name} -l pl.UTF-8
Pakiet uruchomieniowy Ice dla aplikacji w PHP.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%if %{with java}
# we nuke it only when we build new class later, as ice build system expects the file being around
%{__rm} cpp/src/ca/ImportKey.class
%endif

# update path to our install
%{__sed} -i -e 's,/usr/share/Ice-[0-9.]\+,%{_datadir}/Ice,' Ice-rpmbuild-*/icegridregistry.conf
%{__sed} -i -e 's,ln -s Ice-\$(VERSION)/slice,ln -s Ice/slice,' config/Make.common.rules
%{__sed} -i -e 's,ln -s \.\./Ice-\$(VERSION)/slice,ln -s ../Ice/slice,' config/Make.common.rules

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' cpp/config/upgradeicegrid36.py

%build
%if %{with java}
# Rebuild the Java ImportKey class - need it early for main cpp build
javac cpp/src/ca/ImportKey.java
%endif

%{__make} -C cpp \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC -pthread" \
	GCC_COMPILER=yes \
%ifarch x32
	lp64suffix=x32 \
%endif
	embedded_runpath=no

%if %{with gui}
# Create the IceGrid icon
convert java/resources/icons/icegrid.ico temp.png
%{__mv} temp-8.png java/resources/icons/icegrid.png
%{__rm} temp*.png
%endif

%if %{with java}
# Set the CLASSPATH correctly for the Java compile
export CLASSPATH=$(build-classpath db jgoodies-forms jgoodies-looks)

%{__make} -C java \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC -pthread" \
%ifarch x32
	lp64suffix=x32 \
%endif
	embedded_runpath=no
%endif

%if %{with dotnet}
%{__make} -C csharp \
	MCS=dmcs \
%ifarch x32
	lp64suffix=x32 \
%endif
	embedded_runpath=no
%endif

%if %{with python}
%{__make} -C python \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC -pthread" \
%ifarch x32
	lp64suffix=x32 \
%endif
	embedded_runpath=no
%endif

%if %{with ruby}
%{__make} -C ruby \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC -pthread" \
%ifarch x32
	lp64suffix=x32 \
%endif
	embedded_runpath=no
%endif

%if %{with php}
%{__make} -C php \
	PHP_HOME=%{_prefix} \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC -pthread" \
%ifarch x32
	lp64suffix=x32 \
%endif
	embedded_runpath=no
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C cpp install \
%ifarch x32
	lp64suffix=x32 \
%endif
	SLICE_DIR_SYMLINK=yes \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	install_configdir=%{_datadir}/Ice \
	install_docdir=%{_datadir}/Ice \
	install_slicedir=%{_datadir}/Ice/slice

%if %{with java}
%{__make} -C java install \
%ifarch x32
	lp64suffix=x32 \
%endif
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	install_docdir=%{_datadir}/Ice \
	install_slicedir=%{_datadir}/Ice/slice

# Move Java stuff where it should be
install -d $RPM_BUILD_ROOT%{_javadir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/lib/Ice.jar $RPM_BUILD_ROOT%{_javadir}/Ice-%{version}.jar
ln -s Ice-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/Ice.jar
%{__mv} $RPM_BUILD_ROOT%{_prefix}/lib/Freeze.jar $RPM_BUILD_ROOT%{_javadir}/Freeze-%{version}.jar
ln -s Freeze-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/Freeze.jar

# Register ant target
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/ant.d,%{_javadir}/ant}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/lib/ant-ice.jar $RPM_BUILD_ROOT%{_javadir}/ant/ant-ice-%{version}.jar
ln -s ant-ice-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/ant/ant-ice.jar
echo 'ice ant/ant-ice' > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/ice
%endif

%if %{with gui}
# Install the IceGrid GUI
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/lib/IceGridGUI.jar $RPM_BUILD_ROOT%{_datadir}/Ice
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}
cp -a java/resources/icons/icegrid.png $RPM_BUILD_ROOT%{_pixmapsdir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/help/IceGridAdmin $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}
%endif

%if %{with dotnet}
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__make} -C csharp install \
%ifarch x32
	lp64suffix=x32 \
%endif
	GACINSTALL=yes \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	install_pkgconfigdir=%{_pkgconfigdir} \
	install_docdir=%{_datadir}/Ice \
	install_slicedir=%{_datadir}/Ice/slice
%endif

%if %{with python}
%{__make} -C python install \
%ifarch x32
	lp64suffix=x32 \
%endif
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	install_pythondir=%{py_sitedir} \
	install_docdir=%{_datadir}/Ice \
	install_slicedir=%{_datadir}/Ice/slice

%{__mv} $RPM_BUILD_ROOT%{py_sitedir}/IcePy.so{.%{version},}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/IcePy.so.*

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%if %{with ruby}
%{__make} -C ruby install \
%ifarch x32
	lp64suffix=x32 \
%endif
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	install_rubydir=%{ruby_vendorlibdir} \
	install_libdir=%{ruby_vendorarchdir} \
	install_docdir=%{_datadir}/Ice \
	install_slicedir=%{_datadir}/Ice/slice

%{__mv} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/IceRuby.so{.%{version},}
%{__rm} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/IceRuby.so.*
%endif

%if %{with php}
%{__make} -C php install \
%ifarch x32
	lp64suffix=x32 \
%endif
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	install_docdir=%{_datadir}/Ice \
	install_slicedir=%{_datadir}/Ice/slice

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cp -a Ice-rpmbuild-*/ice.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%endif

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/Ice/{ICE_LICENSE,LICENSE}

# Install the servers
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a Ice-rpmbuild-*/*.conf $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
for i in icegridregistry icegridnode glacier2router; do
	cp -a Ice-rpmbuild-*/$i.redhat $RPM_BUILD_ROOT/etc/rc.d/init.d/$i
done
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/icegrid

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n %{php_name}-%{name}
%php_webserver_restart

%postun -n %{php_name}-%{name}
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc ICE_LICENSE CHANGELOG*.md README.md
%attr(755,root,root) %{_bindir}/dumpdb
%attr(755,root,root) %{_bindir}/glacier2router
%attr(755,root,root) %{_bindir}/icebox
%attr(755,root,root) %{_bindir}/iceboxadmin
%attr(755,root,root) %{_bindir}/icegridadmin
%attr(755,root,root) %{_bindir}/icegriddb
%attr(755,root,root) %{_bindir}/icegridnode
%attr(755,root,root) %{_bindir}/icegridregistry
%attr(755,root,root) %{_bindir}/icepatch2calc
%attr(755,root,root) %{_bindir}/icepatch2client
%attr(755,root,root) %{_bindir}/icepatch2server
%attr(755,root,root) %{_bindir}/icestormadmin
%attr(755,root,root) %{_bindir}/icestormdb
%attr(755,root,root) %{_bindir}/icestormmigrate
%attr(755,root,root) %{_bindir}/slice2html
%attr(755,root,root) %{_bindir}/transformdb
%{_mandir}/man1/dumpdb.1*
%{_mandir}/man1/glacier2router.1*
%{_mandir}/man1/icebox.1*
%{_mandir}/man1/iceboxadmin.1*
%{_mandir}/man1/icegridadmin.1*
%{_mandir}/man1/icegriddb.1*
%{_mandir}/man1/icegridnode.1*
%{_mandir}/man1/icegridregistry.1*
%{_mandir}/man1/icepatch2calc.1*
%{_mandir}/man1/icepatch2client.1*
%{_mandir}/man1/icepatch2server.1*
%{_mandir}/man1/icestormadmin.1*
%{_mandir}/man1/icestormdb.1*
%{_mandir}/man1/icestormmigrate.1*
%{_mandir}/man1/slice2html.1*
%{_mandir}/man1/transformdb.1*
%attr(755,root,root) %{_libdir}/libFreeze.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libFreeze.so.%{soversion}
%attr(755,root,root) %{_libdir}/libGlacier2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGlacier2.so.%{soversion}
%attr(755,root,root) %{_libdir}/libGlacier2CryptPermissionsVerifier.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGlacier2CryptPermissionsVerifier.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIce.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIce.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceBox.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceBox.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceDiscovery.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceDiscovery.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceGrid.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceGrid.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceLocatorDiscovery.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceLocatorDiscovery.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIcePatch2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIcePatch2.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceSSL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceSSL.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceStorm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceStorm.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceStormService.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceStormService.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceUtil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceUtil.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceXML.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceXML.so.%{soversion}
%attr(755,root,root) %{_libdir}/libSlice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSlice.so.%{soversion}
%dir %{_datadir}/Ice
%{_datadir}/Ice/slice
%{_datadir}/Ice/icegrid-slice.*.ice.gz
%{_datadir}/Ice/templates.xml
%attr(755,root,root) %{_datadir}/Ice/upgradeicegrid36.py
%{_datadir}/slice

%if %{with gui}
%files -n icegrid-gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/icegridgui
%{_datadir}/Ice/IceGridGUI.jar
%{_mandir}/man1/icegridgui.1*
%{_desktopdir}/IceGridAdmin.desktop
%{_pixmapsdir}/icegrid.png
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/slice2cpp
%attr(755,root,root) %{_bindir}/slice2freeze
%attr(755,root,root) %{_libdir}/libFreeze.so
%attr(755,root,root) %{_libdir}/libGlacier2CryptPermissionsVerifier.so
%attr(755,root,root) %{_libdir}/libGlacier2.so
%attr(755,root,root) %{_libdir}/libIceBox.so
%attr(755,root,root) %{_libdir}/libIceDiscovery.so
%attr(755,root,root) %{_libdir}/libIceGrid.so
%attr(755,root,root) %{_libdir}/libIceLocatorDiscovery.so
%attr(755,root,root) %{_libdir}/libIcePatch2.so
%attr(755,root,root) %{_libdir}/libIce.so
%attr(755,root,root) %{_libdir}/libIceSSL.so
%attr(755,root,root) %{_libdir}/libIceStormService.so
%attr(755,root,root) %{_libdir}/libIceStorm.so
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
%{_includedir}/Slice
%{_mandir}/man1/slice2cpp.1*
%{_mandir}/man1/slice2freeze.1*
%if %{with java}
%{_sysconfdir}/ant.d/ice
%{_javadir}/ant/ant-ice-%{version}.jar
%{_javadir}/ant/ant-ice.jar
%endif

%if %{with dotnet}
%{_pkgconfigdir}/Glacier2.pc
%{_pkgconfigdir}/Ice.pc
%{_pkgconfigdir}/IceBox.pc
%{_pkgconfigdir}/IceDiscovery.pc
%{_pkgconfigdir}/IceGrid.pc
%{_pkgconfigdir}/IceLocatorDiscovery.pc
%{_pkgconfigdir}/IcePatch2.pc
%{_pkgconfigdir}/IceSSL.pc
%{_pkgconfigdir}/IceStorm.pc
%endif

# as we do not have -devel for each binding, these are in main -devel
# -csharp
%attr(755,root,root) %{_bindir}/slice2cs
%{_mandir}/man1/slice2cs.1*
# -java
%attr(755,root,root) %{_bindir}/slice2freezej
%attr(755,root,root) %{_bindir}/slice2java
%{_mandir}/man1/slice2freezej.1*
%{_mandir}/man1/slice2java.1*
# -js
%attr(755,root,root) %{_bindir}/slice2js
%{_mandir}/man1/slice2js.1*
# -php
%attr(755,root,root) %{_bindir}/slice2php
%{_mandir}/man1/slice2php.1*
# -python
%attr(755,root,root) %{_bindir}/slice2py
%{_mandir}/man1/slice2py.1*

%files servers
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/glacier2router.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/icegridnode.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/icegridregistry.conf
%attr(754,root,root) /etc/rc.d/init.d/glacier2router
%attr(754,root,root) /etc/rc.d/init.d/icegridnode
%attr(754,root,root) /etc/rc.d/init.d/icegridregistry

%if %{with dotnet}
%files -n csharp-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/iceboxnet.exe
%{_mandir}/man1/iceboxnet.1*
%{_prefix}/lib/mono/Glacier2
%{_prefix}/lib/mono/Ice
%{_prefix}/lib/mono/IceBox
%{_prefix}/lib/mono/IceDiscovery
%{_prefix}/lib/mono/IceGrid
%{_prefix}/lib/mono/IceLocatorDiscovery
%{_prefix}/lib/mono/IcePatch2
%{_prefix}/lib/mono/IceSSL
%{_prefix}/lib/mono/IceStorm

%{_prefix}/lib/mono/gac/Glacier2
%{_prefix}/lib/mono/gac/Ice
%{_prefix}/lib/mono/gac/IceBox
%{_prefix}/lib/mono/gac/IceDiscovery
%{_prefix}/lib/mono/gac/IceGrid
%{_prefix}/lib/mono/gac/IceLocatorDiscovery
%{_prefix}/lib/mono/gac/IcePatch2
%{_prefix}/lib/mono/gac/IceSSL
%{_prefix}/lib/mono/gac/IceStorm

%{_prefix}/lib/mono/gac/policy.3.6.Glacier2
%{_prefix}/lib/mono/gac/policy.3.6.Ice
%{_prefix}/lib/mono/gac/policy.3.6.IceBox
%{_prefix}/lib/mono/gac/policy.3.6.IceDiscovery
%{_prefix}/lib/mono/gac/policy.3.6.IceGrid
%{_prefix}/lib/mono/gac/policy.3.6.IceLocatorDiscovery
%{_prefix}/lib/mono/gac/policy.3.6.IcePatch2
%{_prefix}/lib/mono/gac/policy.3.6.IceSSL
%{_prefix}/lib/mono/gac/policy.3.6.IceStorm
%endif

%if %{with python}
%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/IcePy.so
%{py_sitedir}/IceBox
%{py_sitedir}/IceGrid
%{py_sitedir}/IceMX
%{py_sitedir}/IcePatch2
%{py_sitedir}/IceStorm
%{py_sitedir}/Glacier2*.py[co]
%{py_sitedir}/Ice.py[co]
%{py_sitedir}/IceBox*.py[co]
%{py_sitedir}/IceGrid*.py[co]
%{py_sitedir}/IcePatch2*.py[co]
%{py_sitedir}/IceStorm*.py[co]
%{py_sitedir}/Ice_*.py[co]
%endif

%if %{with ruby}
%files -n ruby-%{name}
%defattr(644,root,root,755)
%{ruby_vendorlibdir}/Glacier2.rb
%{ruby_vendorlibdir}/Glacier2
%{ruby_vendorlibdir}/Ice.rb
%{ruby_vendorlibdir}/Ice
%{ruby_vendorlibdir}/IceBox.rb
%{ruby_vendorlibdir}/IceBox
%{ruby_vendorlibdir}/IceGrid.rb
%{ruby_vendorlibdir}/IceGrid
%{ruby_vendorlibdir}/IcePatch2.rb
%{ruby_vendorlibdir}/IcePatch2
%{ruby_vendorlibdir}/IceStorm.rb
%dir %{ruby_vendorlibdir}/IceStorm
%{ruby_vendorlibdir}/IceStorm/IceStorm.rb
%{ruby_vendorlibdir}/IceStorm/Metrics.rb
%attr(755,root,root) %{ruby_vendorarchdir}/IceRuby.so
%endif

%if %{with java}
%files -n java-%{name}
%defattr(644,root,root,755)
%{_javadir}/Freeze-%{version}.jar
%{_javadir}/Freeze.jar
%{_javadir}/Ice-%{version}.jar
%{_javadir}/Ice.jar
%endif

%if %{with php}
%files -n %{php_name}-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/ice.ini
%attr(755,root,root) %{php_extensiondir}/IcePHP.so
%{php_data_dir}/Glacier2.php
%{php_data_dir}/Glacier2
%{php_data_dir}/Ice.php
%{php_data_dir}/Ice
%{php_data_dir}/IceBox.php
%{php_data_dir}/IceBox
%{php_data_dir}/IceGrid.php
%{php_data_dir}/IceGrid
%{php_data_dir}/IcePatch2.php
%{php_data_dir}/IcePatch2
%{php_data_dir}/IceStorm.php
%{php_data_dir}/IceStorm
%endif
