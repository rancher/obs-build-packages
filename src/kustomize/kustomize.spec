#
# spec file for package kustomize
#

Name:           kustomize
Version:        5.8.1
Release:        0
Summary:        Customization of kubernetes YAML configurations
License:        Apache-2.0
URL:            https://github.com/kubernetes-sigs/kustomize
Source0:        %{name}-%{version}.tar.zst
Source1:        vendor.tar.zst
BuildRequires:  golang-packaging
BuildRequires:  golang(API) = 1.24
BuildRequires:  zstd

%description
kustomize lets you customize raw, template-free YAML files for multiple
purposes, leaving the original YAML untouched and usable as is.

%prep
%autosetup -p1 -a1 -n %{name}-%{version}

%build
export COMMIT=$(grep "revision" %{_sourcedir}/_service | sed "s/.*\">//; s/<.*//")
export BUILDDATE=$(date +"%Y-%m-%dT%H:%M:%SZ")
export CGO_ENABLED=0
cd kustomize
mv ../vendor .
go build \
    -tags "commit=${COMMIT}|version=v%{version}" \
    -mod=vendor -trimpath \
    -ldflags "\
        -X sigs.k8s.io/kustomize/api/provenance.buildDate=${BUILDDATE} \
        -X sigs.k8s.io/kustomize/api/provenance.version=%{version}" \
    -o %{name} .

%install
cd kustomize
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
