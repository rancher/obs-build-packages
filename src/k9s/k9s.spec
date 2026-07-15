#
# spec file for package k9s
#

Name:           k9s
Version:        0.51.10
Release:        0
Summary:        A Kubernetes CLI to manage your clusters in style
License:        Apache-2.0
URL:            https://github.com/derailed/k9s
Source0:        %{name}-%{version}.tar.zst
Source1:        vendor.tar.zst
BuildRequires:  golang-packaging
BuildRequires:  golang(API) = 1.25
BuildRequires:  zstd

%description
K9s provides a terminal UI to interact with your Kubernetes clusters. The aim of
this project is to make it easier to navigate, observe and manage your
applications in the wild. K9s continually watches Kubernetes for changes and
offers subsequent commands to interact with your observed resources.

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
        -X github.com/derailed/k9s/cmd.version=v%{version} \
        -X github.com/derailed/k9s/cmd.commit=${COMMIT} \
        -X github.com/derailed/k9s/cmd.date=${BUILDDATE}" \
    -o %{name} .

%install
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
