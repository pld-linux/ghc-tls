#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	tls
Summary:	TLS/SSL protocol native implementation (Server and Client)
Name:		ghc-%{pkgname}
Version:	1.5.4
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/tls
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	44202fa7069aa7d04c983787fa015491
URL:		http://hackage.haskell.org/package/tls
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-asn1-encoding
BuildRequires:	ghc-asn1-types >= 0.2.0
BuildRequires:	ghc-async >= 2.0
BuildRequires:	ghc-cereal >= 0.5.3
BuildRequires:	ghc-cryptonite >= 0.25
BuildRequires:	ghc-data-default-class
BuildRequires:	ghc-hourglass
BuildRequires:	ghc-memory >= 0.14.6
BuildRequires:	ghc-network >= 2.4.0.0
BuildRequires:	ghc-transformers
BuildRequires:	ghc-x509 >= 1.7.5
BuildRequires:	ghc-x509-store >= 1.6
BuildRequires:	ghc-x509-validation >= 1.6.5
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-asn1-encoding-prof
BuildRequires:	ghc-asn1-types-prof >= 0.2.0
BuildRequires:	ghc-async-prof >= 2.0
BuildRequires:	ghc-cereal-prof >= 0.5.3
BuildRequires:	ghc-cryptonite-prof >= 0.25
BuildRequires:	ghc-data-default-class-prof
BuildRequires:	ghc-hourglass-prof
BuildRequires:	ghc-memory-prof >= 0.14.6
BuildRequires:	ghc-network-prof >= 2.4.0.0
BuildRequires:	ghc-transformers-prof
BuildRequires:	ghc-x509-prof >= 1.7.5
BuildRequires:	ghc-x509-store-prof >= 1.6
BuildRequires:	ghc-x509-validation-prof >= 1.6.5
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-asn1-encoding
Requires:	ghc-asn1-types >= 0.2.0
Requires:	ghc-async >= 2.0
Requires:	ghc-cereal >= 0.5.3
Requires:	ghc-cryptonite >= 0.25
Requires:	ghc-data-default-class
Requires:	ghc-hourglass
Requires:	ghc-memory >= 0.14.6
Requires:	ghc-network >= 2.4.0.0
Requires:	ghc-transformers
Requires:	ghc-x509 >= 1.7.5
Requires:	ghc-x509-store >= 1.6
Requires:	ghc-x509-validation >= 1.6.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Native Haskell TLS and SSL protocol implementation for server and
client.

This provides a high-level implementation of a sensitive security
protocol, eliminating a common set of security issues through the use
of the advanced type system, high level constructions and common
Haskell features.

Currently implement the SSL3.0, TLS1.0, TLS1.1, TLS1.2 and TLS 1.3
protocol, and support RSA and Ephemeral (Elliptic curve and regular)
Diffie Hellman key exchanges, and many extensions.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-asn1-encoding-prof
Requires:	ghc-asn1-types-prof >= 0.2.0
Requires:	ghc-async-prof >= 2.0
Requires:	ghc-cereal-prof >= 0.5.3
Requires:	ghc-cryptonite-prof >= 0.25
Requires:	ghc-data-default-class-prof
Requires:	ghc-hourglass-prof
Requires:	ghc-memory-prof >= 0.14.6
Requires:	ghc-network-prof >= 2.4.0.0
Requires:	ghc-transformers-prof
Requires:	ghc-x509-prof >= 1.7.5
Requires:	ghc-x509-store-prof >= 1.6
Requires:	ghc-x509-validation-prof >= 1.6.5

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build %{?_smp_mflags}
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Context
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Context/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Context/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Crypto
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Crypto/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Crypto/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Extra
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Extra/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Extra/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Handshake
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Handshake/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Handshake/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Record
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Record/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Record/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Util
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Util/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Util/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Context/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Crypto/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Extra/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Handshake/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Record/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/TLS/Util/*.p_hi
%endif
