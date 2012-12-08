# This sources $HOME/.keychain/$HOSTNAME-sh and
# $HOME/.keychain/$HOSTNAME-sh-gpg, to get the ssh-agent and gpg-agent
# started by keychain.
# Keychain is also started.
# By default keychain will only inherit local agents, if you want it to
# inherit forwarding agents set $KEYCHAIN_OPTIONS in $HOME/.keychain/config
# to something like "--inherit any-once"
#
# You can control behaviour of keychain by setting following variables
# in $HOME/.keychain/config:
#
# KEYCHAIN_OPTIONS
#     Any additional keychain options. 
#
# KEYCHAIN_KEYS
#     List of keys to add on startup. In this case do not try to guess
#     keys here

set KEYCHAIN_OPTIONS=""
set KEYCHAIN_KEYS=""

    if (! $?prompt) then
	set KEYCHAIN_OPTIONS="--noask"
    endif

if (-e "$HOME/.keychain/config")  then
    source "$HOME/.keychain/config"
endif

if ("$KEYCHAIN_KEYS" == "") then
    foreach i (identity id_rsa id_dsa)
	if (-e "$HOME/.ssh/$i") then
	    set KEYCHAIN_KEYS="$KEYCHAIN_KEYS $HOME/.ssh/$i"
	endif
    end

    if ((-e "$HOME/.gnupg/gpg.conf") && ($?GPGKEY == 0)) then
	set GPGKEY=`awk '/^default-key/ {print $2}' "$HOME/.gnupg/gpg.conf"`
	if ("$GPGKEY" == "") then
	    unset GPGKEY
	endif
    endif

    if ((-e "$HOME/.gnupg/pubring.gpg") && ($?GPGKEY == 0)) then
	set GPGKEY=`gpg -K --with-colons | awk -F ':' '$1 == "sec" { print substr($5, 9); exit }'`
	if ("$GPGKEY" == "") then
	    unset GPGKEY
	endif
    endif

    if ($?GPGKEY != 0) then
	set KEYCHAIN_KEYS="$KEYCHAIN_KEYS $GPGKEY"
    endif
endif

if ((-x /usr/bin/keychain) && (-d ~/.keychain)) then
        keychain -q -Q $KEYCHAIN_OPTIONS $KEYCHAIN_KEYS
endif

if ($?HOSTNAME == 0) then
    set HOSTNAME=`/bin/hostname`
endif

set KEYCHAINFILE=$HOME/.keychain/$HOSTNAME-csh

if (-e $KEYCHAINFILE) then 
    source $KEYCHAINFILE
endif

set KEYCHAINFILEGPG=$HOME/.keychain/$HOSTNAME-csh-gpg

if (-e $KEYCHAINFILEGPG) then
    source $KEYCHAINFILEGPG
endif
