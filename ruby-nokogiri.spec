#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	doc			# don't build ri/rdoc

# NOTE
# - changelog https://github.com/sparklemotion/nokogiri/blob/main/CHANGELOG.md

%define	pkgname		nokogiri
Summary:	An HTML, XML, SAX, and Reader parser
Name:		ruby-%{pkgname}
Version:	1.19.1
Release:	2
License:	MIT
Group:		Development/Languages
Source0:	https://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	1e5655ccfbe14ec328dc3bf8eee9b251
Patch0:		%{name}-no-mini_portile2.patch
URL:		https://nokogiri.org/
BuildRequires:	libxml2-devel >= 2.9.2
BuildRequires:	libxslt-devel
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby-devel >= 1:3.2
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	ruby-rdoc
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nokogiri makes it easy and painless to work with XML and HTML from
Ruby. It provides a sensible, easy-to-understand API for reading,
writing, modifying, and querying documents. It is fast and
standards-compliant by relying on native parsers like libxml2,
libgumbo, or xerces.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4
BuildArch:	noarch

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby
BuildArch:	noarch

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%{__tar} xf %{SOURCE0} metadata.gz
gunzip metadata.gz
%__gem_helper spec
# remove mini_portile2 dep from gemspec (not needed with system libraries)
%patch -P0 -p0

%build
export NOKOGIRI_USE_SYSTEM_LIBRARIES=yes

cd ext/nokogiri
%{__ruby} extconf.rb \
	--enable-system-libraries \
	--gumbo-dev
%{__make} \
	CC="%{__cc}" \
	ldflags="%{rpmldflags}" \
	optflags="%{rpmcflags} -fPIC"
cd -

%if %{with doc}
rdoc --op rdoc lib
rdoc --ri --op ri lib
rm -f ri/created.rid
rm -f ri/cache.ri
rm -rf ri/Object
rm -rf ri/lib
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{ruby_vendorlibdir},%{ruby_vendorarchdir}/nokogiri,%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
install -p bin/nokogiri $RPM_BUILD_ROOT%{_bindir}
install -p ext/nokogiri/nokogiri.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/nokogiri
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%if %{with doc}
install -d $RPM_BUILD_ROOT{%{ruby_ridir},%{ruby_rdocdir}}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%attr(755,root,root) %{_bindir}/nokogiri
%{ruby_vendorlibdir}/nokogiri.rb
%{ruby_vendorlibdir}/nokogiri
%{ruby_vendorlibdir}/xsd
%dir %{ruby_vendorarchdir}/nokogiri
%attr(755,root,root) %{ruby_vendorarchdir}/nokogiri/nokogiri.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Nokogiri
%{ruby_ridir}/XSD
%endif
