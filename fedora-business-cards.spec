Name:           fedora-business-cards
Version:        0.3
Release:        1%{?dist}
Summary:        The Fedora business card generator

Group:          Applications/Multimedia
License:        GPLv2+
URL:            https://fedoraproject.org/wiki/Business_cards
Source0:        http://ianweller.fedorapeople.org/releases/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel python-paver python-setuptools python-iniparse
Requires:       PyXML python-fedora ghostscript inkscape aajohan-comfortaa-fonts abattis-cantarell-fonts
Requires:       fedora-logos > 14.0.2-1


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
paver install_executable --root %{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README COPYING
%{python_sitelib}/*
%{_bindir}/%{name}


%changelog
* Thu Jun 16 2011 Ian Weller <ian@ianweller.org> - 0.3-1
- Cards are no longer generated from templates, but are instead generated completely from scratch
- Users can now specify a card size and, optionally, a print bleed in inches or millimeters (RHBZ #480133)
- Cards now use Cantarell and Comfortaa (RHBZ #700397)
- Removes Fedora Talk number (RHBZ #703202)
- Applies Unicode patch from Arturo Fernandez (RHBZ #557001)

* Tue Nov 30 2010 Ian Weller <ian@ianweller.org> - 0.2.4.3-1
- Add template for the Europe business card size

* Sun Jul 25 2010 Ian Weller <iweller@redhat.com> - 0.2.4.2-5
- Rebuilt again for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.2.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Ian Weller <ian@ianweller.org> - 0.2.4.2-2
- Add an appropriate conditional require for inkscape

* Wed Jun 17 2009 Ian Weller <ian@ianweller.org> - 0.2.4.2-1
- Fix pavement.py issues

* Wed Jun 17 2009 Ian Weller <ian@ianweller.org> - 0.2.4.1-1
- Fix bug #502338 (fedora-business-cards generate no PNG)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Ian Weller <ianweller@gmail.com> 0.2.4-3
- Fix F11 dependency on the MgOpen fonts (again)

* Wed Dec 31 2008 Ian Weller <ianweller@gmail.com> 0.2.4-2
- Fix F11 dependency on the MgOpen fonts

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
