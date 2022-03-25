# NOTE: tests spawn >128 processes (ulimit -u 256 is enough)
#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_without	tests		# unit tests
%bcond_with	tests_net	# unit tests requiring network access
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module

%define 	module	Pyro4
Summary:	Distributed object middleware for Python (RPC)
Summary(pl.UTF-8):	Oprogramowanie umożliwiające dystrybucję obiektów w Pythonie (RPC)
Name:		python-%{module}
Version:	4.80
Release:	3
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/Pyro4/
Source0:	https://files.pythonhosted.org/packages/source/P/Pyro4/%{module}-%{version}.tar.gz
# Source0-md5:	e31fc077e06de9fc0bb061e357401954
URL:		https://pypi.org/project/Pyro4/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
%if %{with tests}
BuildRequires:	python-cloudpickle
BuildRequires:	python-dill
BuildRequires:	python-msgpack
BuildRequires:	python-selectors2
BuildRequires:	python-serpent >= 1.27
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
%if %{with tests}
BuildRequires:	python3-cloudpickle
BuildRequires:	python3-dill
BuildRequires:	python3-msgpack
BuildRequires:	python3-serpent >= 1.27
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.5.3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pyro is short for Python Remote Objects. It is an advanced and
powerful Distributed Object Technology system written entirely in
Python, that is designed to be very easy to use.

%description -l pl.UTF-8
Pyro jest skrótem od Python Remote Objects (pythonowe zdalne objekty).
Jest zaawasowanym i poteżnym systemem zarządania zdalnymi obiektami,
napisanym całkowice w Pythonie. Jest zaprojektowany jako bardzo łatwy
w użyciu.

%package -n python3-%{module}
Summary:	Distributed object middleware for Python (RPC)
Summary(pl.UTF-8):	Oprogramowanie umożliwiające dystrybucję obiektów w Pythonie (RPC)
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
Pyro is short for Python Remote Objects. It is an advanced and
powerful Distributed Object Technology system written entirely in
Python, that is designed to be very easy to use.

%description -n python3-%{module} -l pl.UTF-8
Pyro jest skrótem od Python Remote Objects (pythonowe zdalne objekty).
Jest zaawasowanym i poteżnym systemem zarządania zdalnymi obiektami,
napisanym całkowice w Pythonie. Jest zaprojektowany jako bardzo łatwy
w użyciu.

%package apidocs
Summary:	API documentation for Python Pyro4 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona Pyro4
Group:		Documentation

%description apidocs
API documentation for Python Pyro4 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona Pyro4.

%prep
%setup -q -n %{module}-%{version}

# selectors2 is preferred over selectors34, update egg dependency accordingly
%{__sed} -i -e 's/selectors34/selectors2/' setup.py

%if %{without tests_net}
%{__rm} tests/PyroTests/test_{naming,naming2,socket}.py
%endif

%build
%if %{with python2}
%py_build

%if %{with tests}
cd tests
PYTHONPATH=$(pwd)/../src \
%{__python} run_testsuite.py
cd ..
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
cd tests
PYTHONPATH=$(pwd)/../src \
%{__python3} run_testsuite.py
cd ..
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

for bin in check-config flameserver httpgateway ns nsc test-echoserver ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/pyro4-${bin} $RPM_BUILD_ROOT%{_bindir}/pyro4-${bin}-2
done

%py_postclean
%endif

%if %{with python3}
%py3_install

for bin in check-config flameserver httpgateway ns nsc test-echoserver ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/pyro4-${bin} $RPM_BUILD_ROOT%{_bindir}/pyro4-${bin}-3
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/pyro4-check-config-2
%attr(755,root,root) %{_bindir}/pyro4-flameserver-2
%attr(755,root,root) %{_bindir}/pyro4-httpgateway-2
%attr(755,root,root) %{_bindir}/pyro4-ns-2
%attr(755,root,root) %{_bindir}/pyro4-nsc-2
%attr(755,root,root) %{_bindir}/pyro4-test-echoserver-2
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/pyro4-check-config-3
%attr(755,root,root) %{_bindir}/pyro4-flameserver-3
%attr(755,root,root) %{_bindir}/pyro4-httpgateway-3
%attr(755,root,root) %{_bindir}/pyro4-ns-3
%attr(755,root,root) %{_bindir}/pyro4-nsc-3
%attr(755,root,root) %{_bindir}/pyro4-test-echoserver-3
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build/sphinx/html/{_images,_static,api,*.html,*.js}
%endif
