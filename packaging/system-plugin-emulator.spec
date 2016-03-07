Name: system-plugin-emulator
Version: 0.1.7
Release: 1
Summary: System plugin for emulator
License: Apache-2.0
Group: System/Configuration
Requires: udev
Requires: util-linux
Requires: sysvinit
Requires: alsa-utils
Requires(post): setup
Requires(post): coreutils
Source0: %{name}-%{version}.tar.gz
Source1001: packaging/%{name}.manifest
ExclusiveArch: %{ix86} x86_64

%description
System plugin files for emulator

%prep

%setup -q

%build

%install
find . -name .gitignore -exec rm -f {} \;
cp -arf filesystem/* %{buildroot}

# for systemd unit
%install_service basic.target.wants emulator_preinit.target
%install_service emulator_preinit.target.wants emul-setup-audio-volume.service
%install_service emulator_preinit.target.wants emul-common-preinit.service
%install_service emulator_preinit.target.wants dev-disk-by\\x2dlabel-emulator\\x2dswap.swap
%install_service multi-user.target.wants emulator.target
%install_service basic.target.wants tizen-system-env.service

# include license
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}

%posttrans
#run emulator_ns.preinit script after all packages have been installed.
/etc/preconf.d/emulator_ns.preinit

%files
/etc/emulator/prerun
/etc/emulator/prerun.d/set-model-config.sh
/etc/emulator/prerun.d/generate-emulator-env.sh
/etc/inittab
/etc/preconf.d/emulator_ns.preinit
/etc/preconf.d/systemd_conf.preinit
/etc/rc.d/rc.emul
/etc/rc.d/rc.firstboot
/etc/rc.d/rc.shutdown
/etc/rc.d/rc.sysinit
%{_unitdir}/emulator_preinit.target
%{_unitdir}/emulator.target
%{_unitdir}/basic.target.wants/emulator_preinit.target
%{_unitdir}/basic.target.wants/tizen-system-env.service
%{_unitdir}/multi-user.target.wants/emulator.target
%{_unitdir}/emul-setup-audio-volume.service
%{_unitdir}/emul-common-preinit.service
%{_unitdir}/dev-disk-by\x2dlabel-emulator\x2dswap.swap
%{_unitdir}/emulator_preinit.target.wants/emul-setup-audio-volume.service
%{_unitdir}/emulator_preinit.target.wants/emul-common-preinit.service
%{_unitdir}/emulator_preinit.target.wants/dev-disk-by\x2dlabel-emulator\x2dswap.swap
%{_unitdir}/tizen-system-env.service
%{_prefix}/lib/udev/rules.d/51-tizen-udev-default.rules
%{_prefix}/lib/udev/rules.d/95-tizen-emulator.rules
/usr/share/license/%{name}
%{_sysconfdir}/fstab
