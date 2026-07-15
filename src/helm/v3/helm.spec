#
# spec file for package helm (v3)
#

Name:           helm
Version:        3.21.3
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

This package provides the %{name} v3.

%prep
%autosetup -p1 -a1 -n %{name}-%{version}

%build
export COMMIT=$(grep "revision" %{_sourcedir}/_service | sed "s/.*\">//; s/<.*//")
export K8S_MODULE=$(grep k8s.io/client-go go.mod | sed "s/.*v//")
export K8S_MODULES_MAJOR_VER=$(echo $(($(echo ${K8S_MODULE} | cut -d. -f1) + 1)))
export K8S_MODULES_MINOR_VER=$(echo ${K8S_MODULE} | cut -d. -f2 )
export CGO_ENABLED=0
go build \
    -tags "commit=${COMMIT}|version=v%{version}" \
    -mod=vendor -trimpath \
    -ldflags "-s -w \
        -X helm.sh/helm/v3/internal/version.metadata=v%{version} \
        -X helm.sh/helm/v3/internal/version.gitCommit=${COMMIT} \
        -X helm.sh/helm/v3/internal/version.gitTreeState=clean \
        -X helm.sh/helm/v3/pkg/lint/rules.k8sVersionMajor=${K8S_MODULES_MAJOR_VER} \
        -X helm.sh/helm/v3/pkg/lint/rules.k8sVersionMinor=${K8S_MODULES_MINOR_VER} \
        -X helm.sh/helm/v3/pkg/chartutil.k8sVersionMajor=${K8S_MODULES_MAJOR_VER} \
        -X helm.sh/helm/v3/pkg/chartutil.k8sVersionMinor=${K8S_MODULES_MINOR_VER}" \
    -o %{name} ./cmd/helm

%install
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}3

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}3
