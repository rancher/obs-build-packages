#
# spec file for package helm (v4)
#

Name:           helm
Version:        4.2.3
Release:        0
Summary:        The Kubernetes Package Manager 
License:        Apache-2.0
URL:            https://github.com/harvester/docker-machine-driver-harvester
Source0:        %{name}-%{version}.tar.zst
Source1:        vendor.tar.zst
BuildRequires:  golang-packaging
BuildRequires:  golang(API) = 1.26
BuildRequires:  zstd

%description
Helm is a tool for managing Charts. Charts are packages of pre-configured Kubernetes resources.

This package provides the %{name} v4.

%prep
%autosetup -p1 -a1 -n %{name}-%{version}

%build
export COMMIT=$(grep "revision" %{_sourcedir}/_service | sed "s/.*\">//; s/<.*//")
export CGO_ENABLED=0
go build \
    -tags "commit=${COMMIT}|version=v%{version}" \
    -mod=vendor -trimpath \
    -ldflags "-s -w \
        -X helm.sh/helm/v4/internal/version.metadata=v%{version} \
        -X helm.sh/helm/v4/internal/version.gitCommit=${COMMIT} \
        -X helm.sh/helm/v4/internal/version.gitTreeState=clean" \
    -o %{name} ./cmd/helm

%install
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
