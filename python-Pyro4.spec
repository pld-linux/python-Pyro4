%define 	module	Pyro4
Summary:	Distributed object middleware for Python (RPC).
Summary(pl.UTF-8):	Oprogramowanie umożliwiające dystrybucję objektów w Pythonie (RPC).
Name:		python-%{module}
Version:	4.14
Release:	2
License:	MIT
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/P/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	ad096f8e2d58ecac402a58eb6d10531a
URL:		http://packages.python.org/Pyro4/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pyro is short for Python Remote Objects. It is an advanced and
powerful Distributed Object Technology system written entirely in
Python, that is designed to be very easy to use.

%description -l pl.UTF-8
Pyro jest skrótem od Pythonowe zdalne objekty. Jest zaawasowanym i
poteżnym systemem zarządania zdalnymi objektami napisanym całkowice w
Pythonie. Jest zaprojektowany aby być bardzo łatwym w użyciu.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%dir %{py_sitescriptdir}/%{module}/socketserver
%{py_sitescriptdir}/%{module}/socketserver/*.py[co]
%dir %{py_sitescriptdir}/%{module}/test
%{py_sitescriptdir}/%{module}/test/*.py[co]
%dir %{py_sitescriptdir}/%{module}/utils
%{py_sitescriptdir}/%{module}/utils/*.py[co]


%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif
