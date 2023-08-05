Name: libfsapfs
Version: 20190507
Release: 1
Summary: Library to access the Apple File System (APFS) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfsapfs
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         openssl         zlib
BuildRequires: gcc         openssl-devel         zlib-devel

%description -n libfsapfs
Library to access the Apple File System (APFS) format

%package -n libfsapfs-static
Summary: Library to access the Apple File System (APFS) format
Group: Development/Libraries
Requires: libfsapfs = %{version}-%{release}

%description -n libfsapfs-static
Static library version of libfsapfs.

%package -n libfsapfs-devel
Summary: Header files and libraries for developing applications for libfsapfs
Group: Development/Libraries
Requires: libfsapfs = %{version}-%{release}

%description -n libfsapfs-devel
Header files and libraries for developing applications for libfsapfs.

%package -n libfsapfs-python2
Obsoletes: libfsapfs-python < %{version}
Provides: libfsapfs-python = %{version}
Summary: Python 2 bindings for libfsapfs
Group: System Environment/Libraries
Requires: libfsapfs = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libfsapfs-python2
Python 2 bindings for libfsapfs

%package -n libfsapfs-python3
Summary: Python 3 bindings for libfsapfs
Group: System Environment/Libraries
Requires: libfsapfs = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libfsapfs-python3
Python 3 bindings for libfsapfs

%package -n libfsapfs-tools
Summary: Several tools for reading Apple File System (APFS) volumes
Group: Applications/System
Requires: libfsapfs = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libfsapfs-tools
Several tools for reading Apple File System (APFS) volumes

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libfsapfs
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libfsapfs-static
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libfsapfs-devel
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfsapfs.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfsapfs-python2
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libfsapfs-python3
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libfsapfs-tools
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue May  7 2019 Joachim Metz <joachim.metz@gmail.com> 20190507-1
- Auto-generated

