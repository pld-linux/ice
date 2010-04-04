# TODO
# - get stuff from fc spec
# - cc/cflags
# - language bindings
#
# Conditional build:
%bcond_without	java		# Java bindings
%bcond_without	dotnet		# .NET bindings
%bcond_without	python		# Python bindings
%bcond_without	ruby		# Ruby bindings
%bcond_without	php			# PHP bindings
%bcond_without	gui			# IceGrid GUI

Summary:	The Ice base runtime and services
Name:		ice
Version:	3.4.0
Release:	0.2
License:	GPL v2 with exceptions (see ICE_LICENSE)
Group:		Applications
Source0:	http://www.zeroc.com/download/Ice/3.4/Ice-%{version}.tar.gz
# Source0-md5:	998b10627ade020cb00f5beb73efc0e0
# Extracted from http://zeroc.com/download/Ice/3.4/ice-3.4.0-1.src.rpm
Source1:	Ice-rpmbuild-%{version}.tar.gz
# Source1-md5:	869cc60645e7e2b4115584a5ab17d1e9
Source2:	%{name}gridgui
Source3:	IceGridAdmin.desktop
URL:		http://www.zeroc.com/
Patch0:		%{name}-build.patch
Patch1:		dont-build-demo-test.patch
Patch2:		java-build.patch
%{?with_python:BuildRequires:	rpm-pythonprov}
%{?with_ruby:BuildRequires:	ruby >= 1:1.8.6}
Patch3:		jgoodies.patch
BuildRequires:	db-cxx-devel
%{?with_java:BuildRequires:	db-java-devel}
%{?with_java:BuildRequires:	java-jgoodies-forms}
%{?with_java:BuildRequires:	java-jgoodies-looks}
BuildRequires:	mcpp-devel
%{?with_php:BuildRequires:	php-devel >= 3:5.0.0}
BuildRequires:	rpmbuild(macros) >= 1.519
# drop these O/P if not needed
Provides:	Ice
Obsoletes:	Ice
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

%package servers
Summary:	Ice services to run through /etc/rc.d/init.d
Group:		Development/Tools
Requires(post):	/sbin/chkconfig
Requires(pre):	shadow-utils
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires:	%{name} = %{version}-%{release}

%description servers
Ice services to run through /etc/rc.d/init.d

%package devel
Summary:	Tools for developing Ice applications in C++
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# drop these O/P if not needed
Provides:	Ice-devel
Obsoletes:	Ice-devel

%description devel
Tools for developing Ice applications in C++.

%package java
Summary:	The Ice runtime for Java
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	db4-java
Requires:	java >= 1.5.0

%description java
The Ice runtime for Java

%package java-devel
Summary:	Tools for developing Ice applications in Java
Group:		Development/Tools
Requires:	ice-java = %{version}-%{release}

%description java-devel
Tools for developing Ice applications in Java.

%package csharp
Summary:	IceGrid Admin Tool
Summary:	The Ice runtime for C#
Group:		Development/Tools
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Requires:	ice-java = %{version}-%{release}
Requires:	java
Requires:	jgoodies-forms
Requires:	jgoodies-looks
Requires:	jpackage-utils
Requires:	mono-core >= 1.2.2
Provides:	ice-dotnet = %{version}-%{release}
Obsoletes:	ice-dotnet < %{version}-%{release}

%description csharp
The Ice runtime for C#

%package csharp-devel
Summary:	Tools for developing Ice applications in C#
Group:		Development/Tools
Requires:	ice-csharp = %{version}-%{release}
Requires:	pkgconfig

%description csharp-devel
Tools for developing Ice applications in C#.

%package ruby
Summary:	The Ice runtime for Ruby applications
Group:		Development/Tools
BuildRequires:	ruby-modules
Requires:	%{name} = %{version}-%{release}
%{?ruby_mod_ver_requires_eq}

%description ruby
The Ice runtime for Ruby applications.

%package ruby-devel
Summary:	Tools for developing Ice applications in Ruby
Group:		Development/Tools
Requires:	ice-ruby = %{version}-%{release}

%description ruby-devel
Tools for developing Ice applications in Ruby.

%package python
Summary:	The Ice runtime for Python applications
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	python >= 2.3.4

%description python
The Ice runtime for Python applications.

%package python-devel
Summary:	Tools for developing Ice applications in Python
Group:		Development/Tools
Requires:	ice-python = %{version}-%{release}

%description python-devel
Tools for developing Ice applications in Python.

%package php
Summary:	The Ice runtime for PHP applications
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description php
The Ice runtime for PHP applications.

%package php-devel
Summary:	Tools for developing Ice applications in PHP
Group:		Development/Tools
Requires:	ice-php = %{version}-%{release}

%description php-devel
Tools for developing Ice applications in PHP.

%prep
%setup -q -n Ice-%{version} -a 1
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

# Compile the main Ice runtime
# TODO: CC/CXX passing as make param breaks build system
%{__make} -C cpp \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""

%if %{with java}
# Set the CLASSPATH correctly for the Java compile
export CLASSPATH=$(build-classpath db jgoodies-forms jgoodies-looks)

# Rebuild the Java ImportKey class
cd cpp/src/ca
rm *.class
javac ImportKey.java
cd -

%{__make} -C java \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""

# Create the IceGrid icon
cd java/resources/icons
convert icegrid.ico temp.png
mv temp-8.png icegrid.png
rm temp*.png
cd -
%endif

%if %{with dotnet}
%{__make} -C cs \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""
%endif

%if %{with python}
%{__make} -C py \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""
%endif

%if %{with ruby}
%{__make} -C rb \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""
%endif

%if %{with php}
%{__make} -C php \
	PHP_HOME=%{_prefix} \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	embedded_runpath_prefix=""
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_docdir}/Ice-%{version},%{_datadir}/Ice}

%{__make} install \
	prefix=$RPM_BUILD_ROOT \
	GACINSTALL=yes \
	GAC_ROOT=$RPM_BUILD_ROOT%{_libdir} \
	embedded_runpath_prefix=""

%if %{with java}
%{__make} -C java install \
	prefix=$RPM_BUILD_ROOT \
	GACINSTALL=yes \
	GAC_ROOT=$RPM_BUILD_ROOT%{_libdir} \
	embedded_runpath_prefix=""
# Move Java stuff where it should be
install -d $RPM_BUILD_ROOT%{_javadir}
mv $RPM_BUILD_ROOT/lib/ant-ice.jar $RPM_BUILD_ROOT%{_javadir}/ant-ice-%{version}.jar
ln -s ant-ice-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/ant-ice.jar
mv $RPM_BUILD_ROOT/lib/Ice.jar $RPM_BUILD_ROOT%{_javadir}/Ice-%{version}.jar
ln -s Ice-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/Ice.jar
mv $RPM_BUILD_ROOT/lib/Freeze.jar $RPM_BUILD_ROOT%{_javadir}/Freeze-%{version}.jar
ln -s Freeze-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/Freeze.jar
%endif

%if %{with gui}
# Install the IceGrid GUI
mv $RPM_BUILD_ROOT/lib/IceGridGUI.jar $RPM_BUILD_ROOT%{_datadir}/Ice
install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
cp -a java/resources/icons/icegrid.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
install -d $RPM_BUILD_ROOT%{_bindir}
install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_desktopdir}
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
%endif

# Move other rpm-specific files into the right place (README, service stuff)
cp -a Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT/ice.ini

# Install the servers
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a Ice-rpmbuild-%{version}/*.conf $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_initrddir}
for i in icegridregistry icegridnode glacier2router; do
	cp -a Ice-rpmbuild-%{version}/$i.redhat $RPM_BUILD_ROOT%{_initrddir}/$i
done
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/icegrid

# "make install" assumes it's going into a directory under /opt.
# Move things to where they should be in an RPM setting (adapted from
# the original ZeroC srpm).
install -d $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT/include/* $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_libdir}
# There are a couple of files that end up installed in /lib, not %{_libdir},
# so we try this move too.
mv $RPM_BUILD_ROOT/%{_lib}/* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/lib/* $RPM_BUILD_ROOT%{_libdir} || true
mv $RPM_BUILD_ROOT/help/IceGridAdmin $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}

# Copy the man pages into the correct directory
install -d $RPM_BUILD_ROOT%{_mandir}/man1
#cp -a $RPM_BUILD_DIR/Ice-3.3.0-man-pages/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# Fix the encoding and line-endings of all the IceGridAdmin documentation files
cd $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}/IceGridAdmin
chmod a-x *
for f in *.js *.css; do
	dos2unix $f
done
for f in helpman_topicinit.js icegridadmin_navigation.js IceGridAdmin_popup_html.js zoom_pageinfo.js; do
	iconv -f ISO88591 -t UTF8 $f -o $f.tmp
	mv $f.tmp $f
done
cd -

%if %{with dotnet}
# .NET spec files (for csharp-devel) -- convert the paths
for f in IceGrid Glacier2 IceBox Ice IceStorm IcePatch2; do
	sed -i -e "s#/lib/#%{_libdir}/#" $RPM_BUILD_ROOT%{_libdir}/pkgconfig/$f.pc
	sed -i -e "s#mono_root}/usr#mono_root}#" $RPM_BUILD_ROOT%{_libdir}/pkgconfig/$f.pc
	mv $RPM_BUILD_ROOT%{_bindir}/$f.xml $RPM_BUILD_ROOT%{_libdir}/mono/gac/$f/%{version}.*/
done
%endif

%if %{with python}
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
%{__sed} -i -e '1s,/usr/bin/env ruby,%{__ruby},' $RPM_BUILD_ROOT/ruby/*.rb
install -d $RPM_BUILD_ROOT%{ruby_sitearchdir}
mv $RPM_BUILD_ROOT/ruby/IceRuby.so.*.*.* $RPM_BUILD_ROOT%{ruby_sitearchdir}/IceRuby.so
rm -f $RPM_BUILD_ROOT/ruby/IceRuby.so*
mv $RPM_BUILD_ROOT/ruby/* $RPM_BUILD_ROOT%{ruby_sitearchdir}
%endif

%if %{with php}
# Put the PHP stuff into the right place
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir},%{php_data_dir}}
mv $RPM_BUILD_ROOT/ice.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
mv $RPM_BUILD_ROOT/php/IcePHP.so $RPM_BUILD_ROOT%{php_extensiondir}
mv $RPM_BUILD_ROOT/php/* $RPM_BUILD_ROOT%{php_data_dir}
%endif

mv $RPM_BUILD_ROOT/config/* $RPM_BUILD_ROOT%{_datadir}/Ice
mv $RPM_BUILD_ROOT/slice $RPM_BUILD_ROOT%{_datadir}/Ice
# Somehow, some files under "slice" end up with executable permissions -- ??
find $RPM_BUILD_ROOT%{_datadir}/Ice -name "*.ice" | xargs chmod a-x

# Move the ImportKey.class file -- it'll be in %{_libdir} because of the moves earlier
mv $RPM_BUILD_ROOT%{_libdir}/ImportKey.class $RPM_BUILD_ROOT%{_datadir}/Ice

# Move the license files into the documentation directory
mv $RPM_BUILD_ROOT/ICE_LICENSE $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}/ICE_LICENSE
mv $RPM_BUILD_ROOT/LICENSE $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}/LICENSE
# Copy in the other files too
cp CHANGES RELEASE_NOTES  $RPM_BUILD_ROOT%{_docdir}/Ice-%{version}/

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post php
%php_webserver_restart

%postun php
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
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
%attr(755,root,root) %{_bindir}/transformdb
%attr(755,root,root) %{_bindir}/slice2html
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

# XXX gui
%attr(755,root,root) %{_bindir}/icegridgui
%{_desktopdir}/IceGridAdmin.desktop
%{_iconsdir}/hicolor/*/apps/icegrid.png

# XXX doc
%doc %{_docdir}/Ice-%{version}

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

# these pkgconfig files are for csharp, but we do not have separate -devel for csharp
%{_pkgconfigdir}/Glacier2.pc
%{_pkgconfigdir}/Ice.pc
%{_pkgconfigdir}/IceBox.pc
%{_pkgconfigdir}/IceGrid.pc
%{_pkgconfigdir}/IcePatch2.pc
%{_pkgconfigdir}/IceStorm.pc


# as we do not have -devel for each binding, these are in main -devel
# -csharp
%attr(755,root,root) %{_bindir}/slice2cs
# -java
%attr(755,root,root) %{_bindir}/slice2freezej
%attr(755,root,root) %{_bindir}/slice2java
# -php
%attr(755,root,root) %{_bindir}/slice2php
# -python
%attr(755,root,root) %{_bindir}/slice2py
# -ruby
%attr(755,root,root) %{_bindir}/slice2rb

%files servers
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/glacier2router.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/icegridnode.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/icegridregistry.conf
%attr(754,root,root) /etc/rc.d/init.d/glacier2router
%attr(754,root,root) /etc/rc.d/init.d/icegridnode
%attr(754,root,root) /etc/rc.d/init.d/icegridregistry

%files csharp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/iceboxnet.exe
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

%files python
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

%files ruby
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

%files java
%defattr(644,root,root,755)
%{_javadir}/Freeze-%{version}.jar
%{_javadir}/Freeze.jar
%{_javadir}/Ice-%{version}.jar
%{_javadir}/Ice.jar
%{_javadir}/ant-ice-%{version}.jar
%{_javadir}/ant-ice.jar

%files php
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
