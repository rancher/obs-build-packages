#
# spec file for package docker-machine-driver-harvester (v1)
#

Name:           docker-machine-driver-harvester
Version:        1.0.6
Release:        0
Summary:        The Harvester machine driver for Docker
License:        Apache-2.0
URL:            https://github.com/harvester/docker-machine-driver-harvester
Source0:        %{name}-%{version}.tar.zst
Source1:        vendor.tar.zst
BuildRequires:  golang-packaging
BuildRequires:  golang(API) = 1.25
BuildRequires:  zstd

%description
The Harvester machine driver for Docker.

This package provides the %{name} v1.

%prep
%autosetup -p1 -a1 -n %{name}-%{version}

%build
export COMMIT=$(grep revision _service | sed "s/.*\">//; s/<.*//")
export CGO_ENABLED=0
go build \
    -tags commit=${COMMIT} \
    -tags version=v%{version} \
    -mod=vendor -trimpath \
    -ldflags "-extldflags -static -s -w \
        -X main.VERSION=v%{version}" \
    -o %{name} .

%install
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
