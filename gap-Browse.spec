# Automated testing is difficult, since we really want to visually inspect
# the results of the tests.  I have not been able to find a useful automated
# test for this package, so the maintainer should always run this before
# pushing a new version:
#
# gap -l "%%{_gapdir};%%{buildroot}%%{_gapdir}" <<< 'Test("tst/test.tst");'
#
# That test is more useful if the altasrep package is also installed.

Name:           gap-Browse
Version:        1.8.3
Release:        1.0%{?dist}
Summary:        GAP browser for 2-dimensional arrays of data

License:        GPLv3+
URL:            http://www.math.rwth-aachen.de/~Browse/
Source0:        http://www.math.rwth-aachen.de/~Browse/Browse-%{version}.tar.bz2

BuildRequires:  gap-devel
BuildRequires:  ncurses-devel

Requires:       gap-character-tables
Requires:       GAPDoc

Provides:       gap-pkg-Browse = %{version}-%{release}

# Don't Provide the ncurses glue
%global __provides_exclude_from ncurses\\.so

%description
The motivation for this package was to develop functions for an
interactive display of two-dimensional arrays of data, for example
character tables.  They should be displayed with labeled rows and
columns, the display should allow some markup for fonts or colors, it
should be possible to search for entries, to sort rows or columns, to
hide and unhide information, to bind commands to keys, and so on.

To achieve this our package now provides three levels of functionality,
where in particular the first level may also be used for completely
other types of applications:
- A low level interface to ncurses: This may be interesting for all
  kinds of applications which want to display text with some markup and
  colors, maybe in several windows, using the available capabilities of
  a terminal.
- A medium level interface to a generic function NCurses.BrowseGeneric:
  We introduce a new operation Browse which is meant as an interactive
  version of Display for GAP objects.  Then we provide a generic
  function for browsing two-dimensional arrays of data, handles labels
  for rows and columns, searching, sorting, binding keys to actions,
  etc.  This is for users who want to implement new methods for browsing
  two-dimensional data.
- Applications of these interfaces: We provide some applications of the
  ncurses interface and of the function NCurses.BrowseGeneric.  These
  may be interesting for end users, and also as examples for programmers
  of further applications.  This includes a method for browsing
  character tables, several games, and an interface for demos.

%prep
%setup -q -n Browse

# Give an executable script a shebang
sed -i '1i#!/bin/sh' bibl/getnewestbibfile

%build
# This is NOT an autoconf-generated configure script
./configure %{_gap_dir}
make %{?_smp_mflags} CFLAGS="%{optflags}" GAPPATH="%{_gap_dir}"

# Remove an unnecessary script and some leftover build artifacts
rm -f doc/clean doc/main.{pnr,toc}

%install
# There is no install target in the Makefile.
mkdir -p %{buildroot}%{_gap_dir}/pkg
cp -a ../Browse %{buildroot}%{_gap_dir}/pkg

# Remove files that don't need to be installed
rm -f %{buildroot}%{_gap_dir}/pkg/Browse/{CHANGES,README,configure,Makefile*}
rm -fr %{buildroot}%{_gap_dir}/pkg/Browse/src

# Ensure the shared object has proper permissions
find %{buildroot}%{_gap_dir}/pkg/Browse/bin -name \*.so -exec chmod 0755 {} \;

%post -p %{_bindir}/update-gap-workspace

%postun -p %{_bindir}/update-gap-workspace

%files
%doc CHANGES README doc/GPL
%{_gap_dir}/pkg/Browse/

%changelog
* Mon Oct 21 2013 Jerry James <loganjerry@gmail.com> - 1.8.3-1
- New upstream release
- Add missing post and postun scripts

* Wed Aug  7 2013 Jerry James <loganjerry@gmail.com> - 1.8.2-5
- This package needs gap-character-tables at runtime

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Jerry James <loganjerry@gmail.com> - 1.8.2-2
- Don't Provide the shared object
- Fix permissions on the shared object
- Add a note about testing

* Tue Oct 23 2012 Jerry James <loganjerry@gmail.com> - 1.8.2-1
- Initial RPM
