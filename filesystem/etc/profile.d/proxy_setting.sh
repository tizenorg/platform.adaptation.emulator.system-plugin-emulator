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
[ -n "${__proxy}" ] && "ftp_proxy=ftp://${__proxy}/"

__proxy=`cmd_get socks_proxy`
[ -n "${__proxy}" ] && "socks_proxy=socks://${__proxy}/"

export "no_proxy=localhost,127.0.0.1/8,10.0.0.0/16"
