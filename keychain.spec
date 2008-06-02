Name: keychain
Version: 2.6.8
Release: %mkrel 9
Summary: Keychain manages ssh-agent to minimise passphrase entry for ssh
License: GPL
Group: Networking/Remote access
URL: http://www.gentoo.org/proj/en/%{name}/
Source0: http://dev.gentoo.org/~agriffis/keychain/%name-%version.tar.bz2
Source1: %name.profile.sh
Source2: %name.profile.csh
Requires: openssh-askpass openssh-clients 
Requires: gnupg2
BuildArch: noarch
BuildRoot: %_tmppath/%name-%version

%description
Keychain is a manager for OpenSSH, ssh.com, Sun SSH and GnuPG agents.
It acts as a front-end to the agents, allowing you to easily have one
long-running agent process per system, rather than per login session.
This dramatically reduces the number of times you need to enter your
passphrase from once per new login session to once every time your
local machine is rebooted.

Run keychain once manually per user, after which keychain will run (quietly) 
every time you log in (from a profile script).

Hint: If you get tired of keychain, delete ~/.keychain

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_bindir}
install -m 755 %{name} %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_sysconfdir}/profile.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/99%{name}.sh
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/99%{name}.csh
install -d -m 755 %{buildroot}%{_mandir}/man1/
install -m 644 keychain.1 %{buildroot}%{_mandir}/man1/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog 
%_bindir/*
%{_sysconfdir}/profile.d/*
%{_mandir}/man1/%{name}*

