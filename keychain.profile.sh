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

KEYCHAIN_OPTIONS=""
KEYCHAIN_KEYS=""

    case $- in
	*i*) ;;
	*) KEYCHAIN_OPTIONS="--noask" ;;
    esac

[ -e "$HOME/.keychain/config" ] && . "$HOME/.keychain/config"

if [ -z "$KEYCHAIN_KEYS" ]; then
	for i in identity id_rsa id_dsa;do
		[ -e "$HOME/.ssh/$i" ] && KEYCHAIN_KEYS="$KEYCHAIN_KEYS
$HOME/.ssh/$i"
	done

	if [ -e "$HOME/.gnupg/gpg.conf" -a -z "$GPGKEY" ]
	    then GPGKEY=`awk '/^default-key/ {print $2}' "$HOME/.gnupg/gpg.conf"`
	fi
	if [ -e "$HOME/.gnupg/pubring.gpg" -a -z "$GPGKEY" ]
	    then GPGKEY=`gpg -K --with-colons | awk -F ':' '$1 == "sec" { print substr($5, 9); exit }'`
	fi

	[ -n "$GPGKEY" ] && KEYS="$KEYCHAIN_KEYS
$GPGKEY"
fi

if [ -x /usr/bin/keychain -a -d ~/.keychain ]; then
        keychain -q -Q $KEYCHAIN_OPTIONS $KEYCHAIN_KEYS
fi

KEYCHAINFILE=$HOME/.keychain/$HOSTNAME-sh

[ -e $KEYCHAINFILE ] && . $KEYCHAINFILE

KEYCHAINFILEGPG=$HOME/.keychain/$HOSTNAME-sh-gpg

[ -e $KEYCHAINFILEGPG ] && . $KEYCHAINFILEGPG
