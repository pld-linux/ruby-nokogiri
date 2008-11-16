Summary:	an HTML, XML, SAX, and Reader parser. 
Name:		ruby-nokogiri
Version:	1.0.6
Release:	1
License:	Ruby's
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/46796/nokogiri-1.0.6.gem
# Source0-md5:	2c9c5ce6570352edc6a7e6f00e6903da
URL:		http://nokogiri.rubyforge.org/
BuildRequires:	rake
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	setup.rb = 3.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nokogiri is an HTML parser with XPath support for document searching, CSS3
selector support for document searching, an XML/HTML builder, and drop in
replacement for Hpricot (though not bug for bug)

Nokogiri parses and searches XML/HTML very quickly, and also has correctly
implemented CSS3 selector support as well as XPath support.

It also features an Hpricot compatibility layer to help ease the
change to using correct CSS and XPath. 

%prep
%setup -q -c -n nokogiri-%{version}
tar xzf data.tar.gz
cp %{_datadir}/setup.rb .

%build
cd ext/nokogiri
mkdir nokogiri
mv *.c *.h *.rb nokogiri
cd nokogiri
ls *.c *.h > MANIFEST
cd ../../..
ruby setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

ruby setup.rb setup

# rdoc crashes on _why's craaazy code.
#rdoc --op rdoc lib
#rdoc --ri --op ri lib

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_archdir},%{ruby_ridir}}

ruby setup.rb install \
	--prefix=$RPM_BUILD_ROOT

#cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc rdoc
%{ruby_rubylibdir}/nokogiri*
%{ruby_archdir}/nokogiri*
#%{ruby_ridir}/*
