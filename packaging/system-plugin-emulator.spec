Name: system-plugin-emulator
Version: 0.1.7
Release: 1

%define systemd_dir     %{_libdir}/systemd

Summary: System plugin for emulator
License: Apache-2.0
Group: System/Configuration
Requires: udev
Requires: util-linux
Requires: sysvinit
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

# for systemd
# for emulator_preinit.target
mkdir -p %{buildroot}/%{systemd_dir}/system/basic.target.wants
ln -s %{systemd_dir}/system/emulator_preinit.target %{buildroot}/%{systemd_dir}/system/basic.target.wants/
mkdir -p %{buildroot}/%{systemd_dir}/system/emulator_preinit.target.wants
ln -s %{systemd_dir}/system/emul-setup-audio-volume.service %{buildroot}/%{systemd_dir}/system/emulator_preinit.target.wants/
ln -s %{systemd_dir}/system/emul-common-preinit.service %{buildroot}/%{systemd_dir}/system/emulator_preinit.target.wants/
ln -s %{systemd_dir}/system/dev-vdb.swap %{buildroot}/%{systemd_dir}/system/emulator_preinit.target.wants/
# for emulator.target
mkdir -p %{buildroot}/%{systemd_dir}/system/multi-user.target.wants
ln -s %{systemd_dir}/system/emulator.target %{buildroot}/%{systemd_dir}/system/multi-user.target.wants/
ln -s %{systemd_dir}/system/tizen-boot.target %{buildroot}/%{systemd_dir}/system/multi-user.target.wants/
ln -s %{systemd_dir}/system/tizen-system.target %{buildroot}/%{systemd_dir}/system/multi-user.target.wants/
ln -s %{systemd_dir}/system/tizen-runtime.target %{buildroot}/%{systemd_dir}/system/multi-user.target.wants/
mkdir -p %{buildroot}/%{systemd_dir}/system/emulator.target.wants
# services from system-plugin-exynos
ln -s ../tizen-generate-env.service %{buildroot}/%{systemd_dir}/system/basic.target.wants/
mkdir -p %{buildroot}/%{systemd_dir}/system/default.target.wants
ln -s ../tizen-readahead-collect.service %{buildroot}/%{systemd_dir}/system/default.target.wants/
ln -s ../tizen-readahead-replay.service %{buildroot}/%{systemd_dir}/system/default.target.wants/
mkdir -p %{buildroot}/%{systemd_dir}/system/tizen-boot.target.wants
ln -s ../wm_ready.service %{buildroot}/%{systemd_dir}/system/tizen-boot.target.wants/
mkdir -p %{buildroot}/%{systemd_dir}/system/tizen-system.target.wants

# include license
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}

%posttrans
#run emulator_ns.preinit script after all packages have been installed.
/etc/preconf.d/emulator_ns.preinit

%files
/etc/emulator/prerun
/etc/emulator/prerun.d/model-config.sh
/etc/inittab
/etc/preconf.d/emulator_ns.preinit
/etc/preconf.d/systemd_conf.preinit
/etc/profile.d/proxy_setting.sh
/etc/rc.d/rc.emul
/etc/rc.d/rc.firstboot
/etc/rc.d/rc.shutdown
/etc/rc.d/rc.sysinit
%{_libdir}/systemd/system/emulator_preinit.target
%{_libdir}/systemd/system/emulator.target
%{_libdir}/systemd/system/basic.target.wants/emulator_preinit.target
%{_libdir}/systemd/system/basic.target.wants/tizen-generate-env.service
%{_libdir}/systemd/system/default.target.wants/tizen-readahead-collect.service
%{_libdir}/systemd/system/default.target.wants/tizen-readahead-replay.service
%{_libdir}/systemd/system/multi-user.target.wants/emulator.target
%{_libdir}/systemd/system/multi-user.target.wants/tizen-boot.target
%{_libdir}/systemd/system/multi-user.target.wants/tizen-system.target
%{_libdir}/systemd/system/multi-user.target.wants/tizen-runtime.target
%{_libdir}/systemd/system/emul-setup-audio-volume.service
%{_libdir}/systemd/system/emul-common-preinit.service
%{_libdir}/systemd/system/dev-vdb.swap
%{_libdir}/systemd/system/emulator_preinit.target.wants/emul-setup-audio-volume.service
%{_libdir}/systemd/system/emulator_preinit.target.wants/emul-common-preinit.service
%{_libdir}/systemd/system/emulator_preinit.target.wants/dev-vdb.swap
%{_libdir}/systemd/system/tizen-boot.target
%{_libdir}/systemd/system/tizen-system.target
%{_libdir}/systemd/system/tizen-runtime.target
%{_libdir}/systemd/system/tizen-boot.target.wants/wm_ready.service
%{_libdir}/systemd/system/tizen-readahead-collect.service
%{_libdir}/systemd/system/tizen-readahead-replay.service
%{_libdir}/systemd/system/wm_ready.service
%{_libdir}/systemd/system/tizen-generate-env.service
%{_libdir}/udev/rules.d/51-tizen-udev-default.rules
%{_libdir}/udev/rules.d/95-tizen-emulator.rules
/usr/share/license/%{name}
