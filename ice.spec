# TODO
# - finish (pldize) -servers package
#
# Conditional build:
%bcond_without	gui			# IceGrid GUI
%bcond_without	dotnet		# .NET bindings
%bcond_without	java		# Java bindings
%bcond_without	php			# PHP bindings
%bcond_without	python		# Python bindings
%bcond_without	ruby		# Ruby bindings

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%if %{without java}
%undefine	with_gui
%endif

%{?with_java:%include	/usr/lib/rpm/macros.java}
Summary:	The Ice base runtime and services
Name:		ice
Version:	3.4.0
Release:	1
License:	GPL v2 with exceptions (see ICE_LICENSE)
Group:		Applications
URL:		http://www.zeroc.com/
Source0:	http://www.zeroc.com/download/Ice/3.4/Ice-%{version}.tar.gz
# Source0-md5:	998b10627ade020cb00f5beb73efc0e0
# Extracted from http://zeroc.com/download/Ice/3.4/ice-3.4.0-1.src.rpm
Source1:	Ice-rpmbuild-%{version}.tar.gz
# Source1-md5:	869cc60645e7e2b4115584a5ab17d1e9
# Man pages courtesy of Francisco Moya's Debian packages
Source2:	Ice-3.3.0-man-pages.tbz2
# Source2-md5:	c6c17ee1be2e6b615af5b40edae88b75
Source3:	%{name}gridgui
Source4:	IceGridAdmin.desktop
Patch0:		%{name}-build.patch
Patch1:		dont-build-demo-test.patch
Patch2:		java-build.patch
Patch3:		jgoodies.patch
BuildRequires:	bzip2-devel
BuildRequires:	db-cxx-devel
BuildRequires:	expat-devel
BuildRequires:	mcpp-devel
BuildRequires:	openssl-devel
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.533
%if %{with gui}
BuildRequires:	ImageMagick
BuildRequires:	ImageMagick-coder-png
%endif
%if %{with dotnet}
BuildRequires:	mono-csharp
%endif
%if %{with java}
BuildRequires:	ant-nodeps
BuildRequires:	db-java-devel
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
BuildRequires:	java-jgoodies-forms
BuildRequires:	java-jgoodies-looks
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
%endif
%if %{with php}
BuildRequires:	php-devel >= 3:5.0.0
%endif
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
%endif
%if %{with ruby}
BuildRequires:	ruby >= 1:1.8.6
BuildRequires:	ruby-devel
%endif
# Ice doesn't officially support ppc64 at all; sparc64 doesnt have mono
ExcludeArch:	ppc64 sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Some file suffixes we need to grab the right stuff for the file lists
%define		soversion	34

%description
Ice is a modern alternative to object middleware such as CORBA or
COM/DCOM/COM+. It is easy to learn, yet provides a powerful network
infrastructure for demanding technical applications. It features an
object-oriented specification language, easy to use C++, C#, Java,
Python, Ruby, PHP, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic
transport plug-ins, TCP/IP and UDP/IP support, SSL-based security, a
firewall solution, and much more.

%package devel
Summary:	Tools for developing Ice applications in C++
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Tools for developing Ice applications in C++.

%package servers
Summary:	Ice services to run through /etc/rc.d/init.d
Group:		Development/Tools
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description servers
Ice services to run through /etc/rc.d/init.d

%package -n icegrid-gui
Summary:	IceGrid Admin Tool
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	java-%{name} = %{version}-%{release}
Requires:	java-jgoodies-forms
Requires:	java-jgoodies-looks
Requires:	jpackage-utils

%description -n icegrid-gui
Graphical administration tool for IceGrid

%package -n java-%{name}
Summary:	The Ice runtime for Java
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}
Requires:	db-java
Requires:	jpackage-utils

%description -n java-%{name}
The Ice runtime for Java

%package -n csharp-%{name}
Summary:	The Ice runtime for C#
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mono >= 1.2.2

%description -n csharp-%{name}
The Ice runtime for C#

%package -n ruby-%{name}
Summary:	The Ice runtime for Ruby applications
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
%{?ruby_mod_ver_requires_eq}

%description -n ruby-%{name}
The Ice runtime for Ruby applications.

%package -n python-%{name}
Summary:	The Ice runtime for Python applications
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python >= 1:2.3.4

%description -n python-%{name}
The Ice runtime for Python applications.

%package -n php-%{name}
Summary:	The Ice runtime for PHP applications
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description -n php-%{name}
The Ice runtime for PHP applications.

%prep
%setup -q -n Ice-%{version} -a1 -a2
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

# no longer included in 3.4
rm -f *man-pages/slice2docbook.1

# Fix the encoding and line-endings of all the IceGridAdmin documentation files
cd java/resources/IceGridAdmin
%undos *.js *.css
for f in helpman_topicinit.js icegridadmin_navigation.js IceGridAdmin_popup_html.js zoom_pageinfo.js; do
	iconv -f ISO88591 -t UTF8 $f -o $f.tmp
	mv $f.tmp $f
done
cd -

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' cpp/src/ca/iceca

%if %{with java}
# we nuke it only when we build new class later, as ice build system expects the file being around
rm cpp/src/ca/ImportKey.class
%endif

# update path to our install
sed -i -e 's,/usr/share/Ice-%{version},%{_datadir}/Ice,' cpp/src/ca/iceca Ice-rpmbuild-%{version}/icegridregistry.conf

# force our CC/CXX as build system compares for exactly "c++" to setup other rules
sed -i -e 's,c++,%{__cxx},g' cpp/config/Make.rules.Linux

%build
# Compile the main Ice runtime
# TODO: CC/CXX passing as make param breaks build system

%if %{with java}
# Rebuild the Java ImportKey class - need it early for main cpp build
javac cpp/src/ca/ImportKey.java
%endif

%{__make} -C cpp \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""

%if %{with gui}
# Create the IceGrid icon
convert java/resources/icons/icegrid.ico temp.png
mv temp-8.png java/resources/icons/icegrid.png
rm temp*.png
%endif

%if %{with java}

# Set the CLASSPATH correctly for the Java compile
export CLASSPATH=$(build-classpath db jgoodies-forms jgoodies-looks)

%{__make} -C java \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""
%endif

%if %{with dotnet}
%{__make} -C cs \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""
%endif

%if %{with python}
%{__make} -C py \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""
%endif

%if %{with ruby}
%{__make} -C rb \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""
%endif

%if %{with php}
%{__make} -C php \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	PHP_HOME=%{_prefix} \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{_docdir}/Ice-%{version},%{_datadir}/Ice}

%{__make} -C cpp install \
	prefix=$RPM_BUILD_ROOT

# Move the ImportKey.class file
mv $RPM_BUILD_ROOT/lib/ImportKey.class $RPM_BUILD_ROOT%{_datadir}/Ice

mv $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT/include/* $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT/%{_lib}/* $RPM_BUILD_ROOT%{_libdir}

mv $RPM_BUILD_ROOT/config/* $RPM_BUILD_ROOT%{_datadir}/Ice

# Copy the man pages into the correct directory
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -a *man-pages/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%if %{with java}
%{__make} -C java install \
	prefix=$RPM_BUILD_ROOT

# Move Java stuff where it should be
install -d $RPM_BUILD_ROOT%{_javadir}
mv $RPM_BUILD_ROOT/lib/Ice.jar $RPM_BUILD_ROOT%{_javadir}/Ice-%{version}.jar
ln -s Ice-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/Ice.jar
mv $RPM_BUILD_ROOT/lib/Freeze.jar $RPM_BUILD_ROOT%{_javadir}/Freeze-%{version}.jar
ln -s Freeze-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/Freeze.jar

# Register ant target
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/ant.d,%{_javadir}/ant}
mv $RPM_BUILD_ROOT/lib/ant-ice.jar $RPM_BUILD_ROOT%{_javadir}/ant/ant-ice-%{version}.jar
ln -s ant-ice-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/ant/ant-ice.jar
echo 'ice ant/ant-ice' > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/ice
%endif

%if %{with gui}
# Install the IceGrid GUI
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}
mv $RPM_BUILD_ROOT/lib/IceGridGUI.jar $RPM_BUILD_ROOT%{_datadir}/Ice
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}
cp -a java/resources/icons/icegrid.png $RPM_BUILD_ROOT%{_pixmapsdir}
mv $RPM_BUILD_ROOT/help/IceGridAdmin $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}
%endif

%if %{with dotnet}
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__make} -C cs install \
	prefix=$RPM_BUILD_ROOT \
	GACINSTALL=yes \
	GAC_ROOT=$RPM_BUILD_ROOT%{_libdir} \

mv $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT%{_bindir}
# .NET spec files (for csharp-devel) -- convert the paths
for f in IceGrid Glacier2 IceBox Ice IceStorm IcePatch2; do
	sed -i -e "s#/lib/#%{_libdir}/#" $RPM_BUILD_ROOT/lib/pkgconfig/$f.pc
	sed -i -e "s#mono_root}/usr#mono_root}#" $RPM_BUILD_ROOT/lib/pkgconfig/$f.pc
	mv $RPM_BUILD_ROOT/lib/pkgconfig/$f.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/$f.pc
	mv $RPM_BUILD_ROOT%{_bindir}/$f.xml $RPM_BUILD_ROOT%{_libdir}/mono/gac/$f/%{version}.*/
done
%endif

%if %{with python}
%{__make} -C py install \
	prefix=$RPM_BUILD_ROOT
%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' $RPM_BUILD_ROOT/python/Ice.py
install -d $RPM_BUILD_ROOT%{py_sitedir}/Ice
mv $RPM_BUILD_ROOT/python/IcePy.so.*.*.* $RPM_BUILD_ROOT%{py_sitedir}/Ice/IcePy.so
rm -f $RPM_BUILD_ROOT/python/IcePy.so*
mv $RPM_BUILD_ROOT/python/* $RPM_BUILD_ROOT%{py_sitedir}/Ice
cp -a Ice-rpmbuild-%{version}/ice.pth $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%if %{with ruby}
%{__make} -C rb install \
	prefix=$RPM_BUILD_ROOT
%{__sed} -i -e '1s,/usr/bin/env ruby,%{__ruby},' $RPM_BUILD_ROOT/ruby/*.rb
install -d $RPM_BUILD_ROOT%{ruby_sitearchdir}
mv $RPM_BUILD_ROOT/ruby/IceRuby.so.*.*.* $RPM_BUILD_ROOT%{ruby_sitearchdir}/IceRuby.so
rm -f $RPM_BUILD_ROOT/ruby/IceRuby.so*
mv $RPM_BUILD_ROOT/ruby/* $RPM_BUILD_ROOT%{ruby_sitearchdir}
%endif

%if %{with php}
%{__make} -C php install \
	prefix=$RPM_BUILD_ROOT
# Put the PHP stuff into the right place
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir},%{php_data_dir}}
cp -a Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
mv $RPM_BUILD_ROOT/php/IcePHP.so $RPM_BUILD_ROOT%{php_extensiondir}
mv $RPM_BUILD_ROOT/php/* $RPM_BUILD_ROOT%{php_data_dir}
%endif

# move as last, bindings reinstall these if missing
mv $RPM_BUILD_ROOT/slice $RPM_BUILD_ROOT%{_datadir}/Ice

# Move the license files into the documentation directory
mv $RPM_BUILD_ROOT/ICE_LICENSE $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}/ICE_LICENSE
mv $RPM_BUILD_ROOT/LICENSE $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}/LICENSE
# Copy in the other files too
cp CHANGES RELEASE_NOTES  $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}

# Install the servers
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a Ice-rpmbuild-%{version}/*.conf $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_initrddir}
for i in icegridregistry icegridnode glacier2router; do
	cp -a Ice-rpmbuild-%{version}/$i.redhat $RPM_BUILD_ROOT%{_initrddir}/$i
done
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/icegrid

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n php-%{name}
%php_webserver_restart

%postun -n php-%{name}
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_docdir}/Ice-%{version}
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
%attr(755,root,root) %{_bindir}/slice2html
%attr(755,root,root) %{_bindir}/transformdb
%{_mandir}/man1/dumpdb.1*
%{_mandir}/man1/glacier2router.1*
%{_mandir}/man1/icebox.1*
%{_mandir}/man1/iceboxadmin.1*
%{_mandir}/man1/icegridadmin.1*
%{_mandir}/man1/icegridnode.1*
%{_mandir}/man1/icegridregistry.1*
%{_mandir}/man1/icepatch2calc.1*
%{_mandir}/man1/icepatch2client.1*
%{_mandir}/man1/icepatch2server.1*
%{_mandir}/man1/icestormadmin.1*
%{_mandir}/man1/slice2html.1*
%{_mandir}/man1/transformdb.1*
%attr(755,root,root) %{_libdir}/libFreeze.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libFreeze.so.%{soversion}
%attr(755,root,root) %{_libdir}/libGlacier2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGlacier2.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIce.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIce.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceBox.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceBox.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceDB.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceDB.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceGrid.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceGrid.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceGridFreezeDB.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceGridFreezeDB.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIcePatch2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIcePatch2.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceSSL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceSSL.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceStorm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceStorm.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceStormFreezeDB.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceStormFreezeDB.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceStormService.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceStormService.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceUtil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceUtil.so.%{soversion}
%attr(755,root,root) %{_libdir}/libIceXML.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIceXML.so.%{soversion}
%attr(755,root,root) %{_libdir}/libSlice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSlice.so.%{soversion}
%{_datadir}/Ice

%if %{with gui}
# Exclude the stuff that's in IceGrid
%exclude %{_docdir}/Ice-%{version}/IceGridAdmin
%exclude %{_datadir}/Ice/IceGridGUI.jar

%files -n icegrid-gui
%defattr(644,root,root,755)
%doc %{_docdir}/Ice-%{version}/IceGridAdmin
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
%{_pkgconfigdir}/IceGrid.pc
%{_pkgconfigdir}/IcePatch2.pc
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
# -php
%attr(755,root,root) %{_bindir}/slice2php
# -python
%attr(755,root,root) %{_bindir}/slice2py
%{_mandir}/man1/slice2py.1*
# -ruby
%attr(755,root,root) %{_bindir}/slice2rb
%{_mandir}/man1/slice2rb.1*

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
%{_mandir}/man1/iceboxnet.exe.1*
%{_libdir}/mono/Glacier2
%{_libdir}/mono/Ice
%{_libdir}/mono/IceBox
%{_libdir}/mono/IceGrid
%{_libdir}/mono/IcePatch2
%{_libdir}/mono/IceStorm
%{_libdir}/mono/gac/Glacier2
%{_libdir}/mono/gac/Ice
%{_libdir}/mono/gac/IceBox
%{_libdir}/mono/gac/IceGrid
%{_libdir}/mono/gac/IcePatch2
%{_libdir}/mono/gac/IceStorm
%endif

%if %{with python}
%files -n python-%{name}
%defattr(644,root,root,755)
%{py_sitedir}/ice.pth
%dir %{py_sitedir}/Ice
%dir %{py_sitedir}/Ice/IceBox
%dir %{py_sitedir}/Ice/IceGrid
%dir %{py_sitedir}/Ice/IcePatch2
%dir %{py_sitedir}/Ice/IceStorm
%{py_sitedir}/Ice/*.py[co]
%{py_sitedir}/Ice/IceBox/*.py[co]
%{py_sitedir}/Ice/IceGrid/*.py[co]
%{py_sitedir}/Ice/IcePatch2/*.py[co]
%{py_sitedir}/Ice/IceStorm/*.py[co]
%attr(755,root,root) %{py_sitedir}/Ice/IcePy.so
%endif

%if %{with ruby}
%files -n ruby-%{name}
%defattr(644,root,root,755)
%{ruby_sitearchdir}/Glacier2.rb
%{ruby_sitearchdir}/Glacier2
%{ruby_sitearchdir}/Ice.rb
%{ruby_sitearchdir}/Ice
%{ruby_sitearchdir}/IceBox.rb
%{ruby_sitearchdir}/IceBox
%{ruby_sitearchdir}/IceGrid.rb
%{ruby_sitearchdir}/IceGrid
%{ruby_sitearchdir}/IcePatch2.rb
%{ruby_sitearchdir}/IcePatch2
%{ruby_sitearchdir}/IceStorm.rb
%{ruby_sitearchdir}/IceStorm/IceStorm.rb
%attr(755,root,root) %{ruby_sitearchdir}/IceRuby.so
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
%files -n php-%{name}
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
