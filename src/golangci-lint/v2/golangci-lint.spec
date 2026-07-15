#
# spec file for package golangci-lint (v2)
#

Name:           golangci-lint
Version:        2.12.2
Release:        0
Summary:        Fast linters runner for Go
License:        GPL-3.0
URL:            https://github.com/golangci/golangci-lint
Source0:        %{name}-%{version}.tar.zst
Source1:        vendor.tar.zst
BuildRequires:  golang-packaging
BuildRequires:  golang(API) = 1.26
BuildRequires:  zstd

%description
golangci-lint is a fast Go linters runner.

It runs linters in parallel, uses caching, supports YAML configuration, integrates with all major IDEs, and includes over a hundred linters.

%prep
%autosetup -p1 -a1 -n %{name}-%{version}

%build
export COMMIT=$(grep "revision" %{_sourcedir}/_service | sed "s/.*\">//; s/<.*//")
export BUILDDATE=$(date +"%Y-%m-%dT%H:%M:%SZ")
export CGO_ENABLED=0
go build \
    -tags "commit=${COMMIT}|version=v%{version}" \
    -mod=vendor -trimpath \
    -ldflags "-s -w \
        -X main.version=v%{version} \
        -X main.commit=${COMMIT} \
        -X main.date=${BUILDDATE}" \
    -o %{name} ./cmd/%{name}

%install
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
