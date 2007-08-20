%define name camserv
%define version 0.5.1
%define release %mkrel 1

Summary: A streaming web video server
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownloads.sourceforge.net/cserv/%{name}-%{version}.tar.bz2
Patch0: camserv-0.5.1-errno.patch.bz2
# Patch1 and Patch2 based on Thomas Vander Stichele's Fedora package
Patch1: camserv-0.5.1-gdk-pixbuf.patch.bz2
Patch2: camserv-0.5.1-config.patch.bz2
License: GPL
Group: System/Kernel and hardware
Url: http://cserv.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: jpeg-devel imlib2-devel gdk-pixbuf-devel
BuildRequires: automake1.7 autoconf2.5

%description
Camserv is a streaming web video server. It provides functionality for
unlimited image manipulation before being streamed, in addition to
relay support.

%prep
%setup -q
%patch0 -p1 -b .errno
%patch1 -p1 -b .gdk-pixbuf
%patch2 -p1 -b .config
# regenerate libltdl configure
# because old configure 2.13 doesn't support topdir's configure arguments
pushd libltdl
  rm -f configure
  aclocal-1.7 -I ../macros
  autoconf-2.5x
  automake-1.7
popd

%build
(cd libltdl; %configure2_5x)
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# camserv has been patched to find the config in /etc
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}.cfg $RPM_BUILD_ROOT%{_sysconfdir}

# relay is a quite generic name, rename as camserv-relay
mv $RPM_BUILD_ROOT%{_bindir}/{relay,%{name}-relay}

# remove devel files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING ChangeLog NEWS README TODO javascript.txt
%{_bindir}/%{name}
%{_bindir}/%{name}-relay
%config(noreplace) %{_sysconfdir}/camserv.cfg
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lib*.so*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/defpage.html
