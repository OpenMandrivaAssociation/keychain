Name:		keychain
Version:	2.7.1
Release:	6
Summary:	Keychain manages ssh-agent to minimise passphrase entry for ssh
License:	GPLv2
Group:		Networking/Remote access
URL:		http://www.funtoo.org/en/security/%{name}/intro
Source0:	http://www.funtoo.org/archive/%{name}/%name-%version.tar.bz2
Source1:	%{name}.profile.sh
Source2:	%{name}.profile.csh
#Patch500:	keychain-2.6.8-parse_gpg_keys.patch
Suggests:	openssh-askpass
Requires:	openssh-clients
Requires:	gnupg2
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Keychain is a manager for OpenSSH, ssh.com, Sun SSH and GnuPG agents.
It acts as a front-end to the agents, allowing you to easily have one
long-running agent process per system, rather than per login session.
This dramatically reduces the number of times you need to enter your
passphrase from once per new login session to once every time your
local machine is rebooted.

Run keychain once manually per user, after which keychain will run (quietly)
every time you log in (from a profile script).

Hint: If you get tired of keychain, delete ~/.keychain .

%prep
%setup -q
#%patch500 -p1 -b .parse_gpg_keys

%build
%make

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
%doc README.rst ChangeLog COPYING.txt keychain.pod keychain.txt
%{_bindir}/*
%{_sysconfdir}/profile.d/*
%{_mandir}/man1/%{name}*


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.7.1-4mdv2011.0
+ Revision: 666025
- mass rebuild

* Thu Sep 16 2010 Funda Wang <fwang@mandriva.org> 2.7.1-3mdv2011.0
+ Revision: 579003
- fix mdv#61036

* Tue Sep 07 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2.7.1-2mdv2011.0
+ Revision: 576634
- Fix keychain invocation with --noask so that it doesn't trigger ssh-askpass
  dialogue before a window manager is started, i.e. --noask is always used when
  the shell is non-interactive. (bash and csh magic borrowed from Fedora).
  Should fix (mdv#58484).

* Tue Aug 03 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2.7.1-1mdv2011.0
+ Revision: 565193
- update to 2.7.1

* Mon Dec 28 2009 Ahmad Samir <ahmadsamir@mandriva.org> 2.7.0-1mdv2010.1
+ Revision: 482994
- update to 2.7.0
- man page now keychain.1.gz

* Sun Aug 09 2009 Emmanuel Andry <eandry@mandriva.org> 2.6.9-1mdv2010.0
+ Revision: 412975
- New version 2.6.9
- Fix Url and Source Url
- update files list

* Thu Feb 19 2009 Olivier Blin <oblin@mandriva.com> 2.6.8-18mdv2009.1
+ Revision: 342879
- fix csh profile syntax (from darkc and Konrad Bernlohr, #47294)

* Thu Feb 19 2009 Jérôme Soyer <saispo@mandriva.org> 2.6.8-17mdv2009.1
+ Revision: 342798
- Move openssh-askpass to Suggests and not to Requires

* Sat Jan 24 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 2.6.8-16mdv2009.1
+ Revision: 333325
- Adding GPG key in keychain is of little gain - it will eventually timeout
  and key dialog every time new shell is started quickly becomes annoying.
  So to make it configurable and preserve compatibility:
  * remove patch501, patch502
  * use KEYCHAIN_KEYS as list of keys to load. If it is defined (e.g. in
  ~/.keychain/config, usual autodetection of keys is skipped.

* Thu Jan 08 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 2.6.8-15mdv2009.1
+ Revision: 327133
- patch502: fix false warning about missing keys

* Tue Jan 06 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 2.6.8-14mdv2009.1
+ Revision: 325509
- patch501: GPG keys were never loaded by keychain in graphic session
- patch500: fix parsing of GPG keys; use the idea from profile.d script
- fix gpg keys parsing in 99keychain.(c|)sh. It was returning the first
  record ever, not necessarily the first private key.

* Tue Nov 25 2008 Helio Chissini de Castro <helio@mandriva.com> 2.6.8-13mdv2009.1
+ Revision: 306574
- Add the other possible options in post dialog for current kde.

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 2.6.8-12mdv2009.0
+ Revision: 264763
- rebuild early 2009.0 package (before pixel changes)

* Wed Jun 04 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.6.8-11mdv2009.0
+ Revision: 215016
- add --noask option for Xfce session
- spec file clean
- new license policy

* Mon Jun 02 2008 Helio Chissini de Castro <helio@mandriva.com> 2.6.8-10mdv2009.0
+ Revision: 214410
- Fixing right KDE 4 entry.
- Let's  make AdamW happy. adding Gnome on --nokey test

* Mon Jun 02 2008 Helio Chissini de Castro <helio@mandriva.com> 2.6.8-9mdv2009.0
+ Revision: 214265
- Grmbl, the lack of space on shell comparison was breaking other desktops than kde to working with askpass. Thanks fo G?\195?\182tz to spot the fail and Blino for fix

* Thu May 29 2008 Helio Chissini de Castro <helio@mandriva.com> 2.6.8-8mdv2009.0
+ Revision: 213091
- Add --noask for desktop session logins to avoid have a dialog before some window manager starts. Solution added for kde desktops. In other situations, the regular behavior is maintained.

* Mon Mar 17 2008 Olivier Blin <oblin@mandriva.com> 2.6.8-7mdv2008.1
+ Revision: 188328
- if no default-key is specified in gpg.conf, ask password for first private key
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Nov 29 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.6.8-6mdv2008.1
+ Revision: 113959
- don't set executable bit on profile scriplet, they are sourced (fix #25374)

* Sat Nov 17 2007 Funda Wang <fwang@mandriva.org> 2.6.8-5mdv2008.1
+ Revision: 109224
- rebuild for new lzma

* Mon Oct 29 2007 Nicholas Brown <nickbrown@mandriva.org> 2.6.8-4mdv2008.1
+ Revision: 103650
- fix bug #25374

* Fri Sep 21 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 2.6.8-3mdv2008.0
+ Revision: 91863
- revert fix for #25374 (don't install profile script as executables).
  It caused a regression because /etc/bashrc is sourcing executable files from
  /etc/profile.d/. (BTW, the fix, which was commited in january, appeared on
  the mirrors only this week). See the discussion on bug #33839.


* Thu Jan 25 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.6.8-2mdv2007.0
+ Revision: 113346
- don't install profile script as executables (fix #25374)

* Mon Nov 27 2006 Nicholas Brown <nickbrown@mandriva.org> 2.6.8-1mdv2007.1
+ Revision: 87549
- new version
- New version
- New version
- Import keychain

* Mon Jul 31 2006 Helio Castro <helio@mandriva.com> 2.6.2-2mdv2007.0
- Added numbering scheme for profiles, allowing keychain profiles been 
the last profile read after ask-pass profile scripts

* Fri Mar 31 2006 Nick Brown <nickbrown@mandriva.org> 2.6.2-1mdk
- 2.6.2

* Sat Oct 15 2005 Nick Brown <nickbrown@mandriva.org> 2.6.1-1mdk
- 2.6.1
- make profile script zsh compatible (#14804)

* Tue Sep 20 2005 Nick Brown <nickbrown@mandriva.org> 2.5.5-2mdk
- Add csh profile.d script (#18698)
- %%{_sysconfdir}/profile.d/ files are not %%config files
- shellbang in %%{_sysconfdir}/profile.d/ files

* Thu Aug 04 2005 Nick Brown <nickbrown@mandriva.org> 2.5.5-1mdk
- 2.5.5
- use %%mkrel

* Thu May 19 2005 Nick Brown <nickbrown@mandrake.org> 2.5.4.1-1mdk
- 2.5.4.1
- Fixed URL

* Wed Mar 30 2005 Nick Brown <nickbrown@mandrake.org> 2.5.3.1-1mdk
- 2.5.3.1

* Wed Feb 02 2005 Nick Brown <nickbrown@mandrake.org> 2.5.1-1mdk
- 2.5.1
- added gpg keys to keychain's keylist
- KEYCHAIN_OPTIONS in .keychain/config to override agent inheriting behaviour

* Thu Nov 25 2004 Nick Brown <nickbrown@mandrake.org> 2.4.3-1mdk
- 2.4.3 (now with gpg-agent support)
- update spec description
- source gpg-agent info in profile script

* Sun Jun 27 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.3.4-1mdk
- 2.3.4

* Thu Jun 10 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.3.1-1mdk
- 2.3.1

* Fri Apr 30 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.2.0-1mdk
- 2.2.0
- Use new -Q option in profile script (speed up logins/new shells)
- add new man page
- spec file cosmetics

