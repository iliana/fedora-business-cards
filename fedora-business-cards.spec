%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           fedora-business-cards
Version:        0.2
Release:        2%{?dist}
Summary:        A tool for rendering Fedora contributor business cards

Group:          Applications/Multimedia
License:        GPLv2+
URL:            https://fedoraproject.org/wiki/Business_cards
Source0:        http://ianweller.fedorapeople.org/releases/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-paver
Requires:       mgopen-fonts inkscape PyXML python-iniparse pygpgme python-fedora


%description
fedora-business-cards is a tool written in Python to generate business cards
for Fedora Project contributors.


%prep
%setup -q


%build
paver build


%install
rm -rf %{buildroot}
paver install --skip-build --root %{buildroot}
paver install_templates --root %{buildroot}
paver install_executable --root %{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README COPYING ChangeLog
%{python_sitelib}/*
%{_bindir}/%{name}
%{_datadir}/%{name}


%changelog
* Mon Oct 06 2008 Ian Weller <ianweller@gmail.com> 0.2-2
- Fix Source0 URL (fedorapeople.org doesn't do https)

* Mon Oct 06 2008 Ian Weller <ianweller@gmail.com> 0.2-1
- Initial package build.
