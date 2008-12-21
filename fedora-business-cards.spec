%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           fedora-business-cards
Version:        0.2.4
Release:        1%{?dist}
Summary:        The Fedora business card generator

Group:          Applications/Multimedia
License:        GPLv2+
URL:            https://fedoraproject.org/wiki/Business_cards
Source0:        http://ianweller.fedorapeople.org/releases/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel python-paver python-setuptools python-iniparse
Requires:       mgopen-fonts inkscape PyXML python-iniparse pygpgme python-fedora ghostscript


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
paver install_data --root %{buildroot}
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
* Sun Dec 21 2008 Ian Weller <ianweller@gmail.com> 0.2.4-1
- Add CMYK PDF as an export option

* Sun Dec 14 2008 Ian Weller <ianweller@gmail.com> 0.2.3-1
- Add EPS as an export option

* Sun Dec 14 2008 Ian Weller <ianweller@gmail.com> 0.2.2-3
- Change summary to be more helpful

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.2-2
- Rebuild for Python 2.6

* Sun Nov 09 2008 Ian Weller <ianweller@gmail.com> 0.2.2-1
- Fix coloration in back templates

* Thu Oct 30 2008 Ian Weller <ianweller@gmail.com> 0.2.1-1
- Upstream update

* Mon Oct 06 2008 Ian Weller <ianweller@gmail.com> 0.2-3
- Fix BuildRequires

* Mon Oct 06 2008 Ian Weller <ianweller@gmail.com> 0.2-2
- Fix Source0 URL (fedorapeople.org doesn't do https)

* Mon Oct 06 2008 Ian Weller <ianweller@gmail.com> 0.2-1
- Initial package build.
