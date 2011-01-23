
%define gitrev 6dbda31
%define gitauthor tenderlove
%define gitproject nokogiri

Summary:	An HTML, XML, SAX, and Reader parser
Name:		ruby-nokogiri
Version:	1.4.3.1
Release:	1
License:	Ruby's
Group:		Development/Languages
Source0:	http://download.github.com/%{gitauthor}-%{gitproject}-REL_%{version}-0-g%{gitrev}.tar.gz
# Source0-md5:	520dec8ef8ac1c7ca42f508ed016784d
Patch0:		%{name}-binpath.patch
URL:		http://nokogiri.org/
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	ruby-devel
BuildRequires:	setup.rb >= 3.4.1
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nokogiri is an HTML parser with XPath support for document searching,
CSS3 selector support for document searching, an XML/HTML builder, and
drop in replacement for Hpricot (though not bug for bug).

Nokogiri parses and searches XML/HTML very quickly, and also has
correctly implemented CSS3 selector support as well as XPath support.

It also features an Hpricot compatibility layer to help ease the
change to using correct CSS and XPath.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{gitauthor}-%{gitproject}-17c2ced
%patch0 -p1
find -newer README.rdoc -o -print | xargs touch --reference %{SOURCE0}
cp %{_datadir}/setup.rb .
ruby setup.rb config \
	--installdirs=std
ruby setup.rb setup

racc -l -o lib/nokogiri/css/generated_parser.rb lib/nokogiri/css/parser.y
rex --independent -o lib/nokogiri/css/generated_tokenizer.rb lib/nokogiri/css/tokenizer.rex

rdoc --op rdoc lib
rdoc --ri --op ri lib
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_archdir},%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}

ruby setup.rb install \
	--prefix=$RPM_BUILD_ROOT

cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rdoc README.rdoc
%attr(755,root,root) %{_bindir}/nokogiri
%{ruby_rubylibdir}/nokogiri*
%{ruby_rubylibdir}/xsd
%{ruby_archdir}/nokogiri*

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Nokogiri
%{ruby_ridir}/XSD
