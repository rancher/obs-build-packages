#
# spec file for package kubectl v1.35
#

Name:           kubectl1.35
Version:        1.35.6
Release:        0
Summary:        Kubernetes command-line tool
License:        Apache-2.0
URL:            https://github.com/kubernetes/kubernetes
Source0:        %{name}-%{version}.tar.zst
BuildRequires:  golang-packaging
BuildRequires:  golang(API) = 1.25
BuildRequires:  zstd

%description
kubectl is the command-line client for Kubernetes. It lets you run commands
against K8s clusters - deploy applications, inspect resources, and manage
cluster components.

This package provides the kubectl binary from the v1.36 release line, built out
of the upstream kubernetes/kubernetes monorepo at the corresponding tag.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
export COMMIT=$(grep "revision" %{_sourcedir}/_service | sed "s/.*\">//; s/<.*//")
export BUILDDATE=$(date +"%Y-%m-%dT%H:%M:%SZ")
export K8S_MAJOR_VERSION=$(echo %{version} | sed "s/\..*//")
export K8S_MINOR_VERSION=$(echo %{version} | sed "s/[0-9]\+\.//; s/\..*//")
export CGO_ENABLED=0
go build \
    -tags "commit=${COMMIT}|version=v%{version}" \
    -mod=vendor -trimpath \
    -ldflags "-s -w \
        -X k8s.io/client-go/pkg/version.buildDate=${BUILDDATE} \
        -X k8s.io/component-base/version.buildDate=${BUILDDATE} \
        -X k8s.io/client-go/pkg/version.gitCommit=${COMMIT} \
        -X k8s.io/component-base/version.gitCommit=${COMMIT} \
        -X k8s.io/client-go/pkg/version.gitTreeState=clean \
        -X k8s.io/component-base/version.gitTreeState=clean \
        -X k8s.io/client-go/pkg/version.gitVersion=v%{version} \
        -X k8s.io/component-base/version.gitVersion=v%{version} \
        -X k8s.io/client-go/pkg/version.gitMajor=${K8S_MAJOR_VERSION} \
        -X k8s.io/component-base/version.gitMajor=${K8S_MAJOR_VERSION} \
        -X k8s.io/client-go/pkg/version.gitMinor=${K8S_MINOR_VERSION} \
        -X k8s.io/component-base/version.gitMinor=${K8S_MINOR_VERSION}" \
    -o %{name} ./cmd/%{name}

%install
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
