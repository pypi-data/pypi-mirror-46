%global pythonv python3
%global srcname statusinfo

Name:           %{srcname}
Version:        0.1.3
Release:        1%{?dist}
Summary:        A tool for gathering status information
License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
#Source0:        %%pypi_source
Source0:        https://files.pythonhosted.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  %{pythonv}-devel
BuildRequires:  %{pythonv}-setuptools
BuildRequires:  %{pythonv}-setuptools_scm

%description
%{summary}.

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.rst
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Sun May 05 2019 eikendev <raphael@eiken.dev> - 0.1.3-1
- Update to 0.1.3

* Sat May 04 2019 eikendev <raphael@eiken.dev> - 0.1.2-1
- Update to 0.1.2

* Sat May 04 2019 eikendev <raphael@eiken.dev> - 0.1.1-1
- Update to 0.1.1

* Thu May 02 2019 eikendev <raphael@eiken.dev> - 0.1.0-1
- Initial package
