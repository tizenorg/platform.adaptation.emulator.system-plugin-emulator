#!/bin/sh

function cmd_get
{
	cat /proc/cmdline | tr -s [:space:] '\n' | grep -m1 "^$1=" | cut -d= -f2
}

__proxy=`cmd_get http_proxy`
[ -n "${__proxy}" ] && export "http_proxy=http://${__proxy}/"

__proxy=`cmd_get https_proxy`
[ -n "${__proxy}" ] && export "https_proxy=https://${__proxy}/"

__proxy=`cmd_get ftp_proxy`
[ -n "${__proxy}" ] && export "ftp_proxy=ftp://${__proxy}/"

__proxy=`cmd_get socks_proxy`
[ -n "${__proxy}" ] && export "socks_proxy=socks://${__proxy}/"

no_proxy="localhost,127.0.0.1/8,10.0.0.0/16"

# Work around for bug in zypper, not handling netmasks in no_proxy.
# Exlicitly add default gateway ip to no_proxy.
__gw=`cmd_get ip | cut -d: -f3`
[ -n "${__gw}" ] && no_proxy="${no_proxy},${__gw}"

export no_proxy
