#
# spec file for package yq
#

Name:           yq
Version:        4.53.3
Release:        0
Summary:        A portable command-line YAML processor 
License:        MIT
URL:            https://github.com/mikefarah/yq
Source0:        %{name}-%{version}.tar.zst
Source1:        vendor.tar.zst
BuildRequires:  golang-packaging
BuildRequires:  golang(API) = 1.25
BuildRequires:  zstd

%description
yq is a portable command-line YAML, JSON, XML, CSV, TOML, HCL and properties
processor.

%prep
%autosetup -p1 -a1 -n %{name}-%{version}

%build
export COMMIT=$(grep "revision" %{_sourcedir}/_service | sed "s/.*\">//; s/<.*//")
export CGO_ENABLED=0
go build \
    -tags "commit=${COMMIT}|version=v%{version}" \
    -mod=vendor -trimpath \
    -ldflags "-s -w " \
    -o %{name} .

%install
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
