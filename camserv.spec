%define name camserv
%define version 0.5.1
%define release %mkrel 5

Summary: A streaming web video server
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownloads.sourceforge.net/cserv/%{name}-%{version}.tar.bz2
Patch0: camserv-0.5.1-errno.patch
# Patch1 and Patch2 based on Thomas Vander Stichele's Fedora package
Patch1: camserv-0.5.1-gdk-pixbuf.patch
Patch2: camserv-0.5.1-config.patch
License: GPL
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: https://cserv.sourceforge.net/
BuildRequires: jpeg-devel imlib2-devel

%description
Camserv is a streaming web video server. It provides functionality for
unlimited image manipulation before being streamed, in addition to
relay support.

%prep
%setup -q
%patch0 -p1 -b .errno
%patch1 -p1 -b .gdk-pixbuf
%patch2 -p1 -b .config

%build
autoreconf -fi
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
