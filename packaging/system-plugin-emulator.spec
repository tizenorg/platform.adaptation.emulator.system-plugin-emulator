Name: system-plugin-emulator
Version: 0.0.16
Release: 1

%define systemd_dir     /usr/lib/systemd

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

%description
System plugin files for emulator

%prep

%setup -q

%build

%install
find . -name .gitignore -exec rm -f {} \;
cp -arf filesystem/* %{buildroot}

# for legacy init
if [ ! -d %{buildroot}/etc/rc.d/rc3.d ]; then
    mkdir -p %{buildroot}/etc/rc.d/rc3.d
fi
ln -s /etc/init.d/setup-audio-volume %{buildroot}//etc/rc.d/rc3.d/S02setup-audio-volume
ln -s /etc/init.d/mount-hostdir %{buildroot}//etc/rc.d/rc3.d/S03mount-hostdir

# for systemd
# for emulator_preinit.target
mkdir -p %{buildroot}/%{systemd_dir}/system/basic.target.wants
ln -s %{systemd_dir}/system/emulator_preinit.target %{buildroot}/%{systemd_dir}/system/basic.target.wants/
mkdir -p %{buildroot}/%{systemd_dir}/system/emulator_preinit.target.wants
ln -s %{systemd_dir}/system/emul-setup-audio-volume.service %{buildroot}/%{systemd_dir}/system/emulator_preinit.target.wants/
ln -s %{systemd_dir}/system/emul-mount-hostdir.service %{buildroot}/%{systemd_dir}/system/emulator_preinit.target.wants/
ln -s %{systemd_dir}/system/emul-common-preinit.service %{buildroot}/%{systemd_dir}/system/emulator_preinit.target.wants/
ln -s %{systemd_dir}/system/dev-vdb.swap %{buildroot}/%{systemd_dir}/system/emulator_preinit.target.wants/
# for emulator.target
mkdir -p %{buildroot}/%{systemd_dir}/system/multi-user.target.wants
ln -s %{systemd_dir}/system/emulator.target %{buildroot}/%{systemd_dir}/system/multi-user.target.wants/
mkdir -p %{buildroot}/%{systemd_dir}/system/emulator.target.wants

# services from system-plugin-exynos
rm %{buildroot}/%{systemd_dir}/system/tizen-generate-env.service

mkdir -p %{buildroot}/%{systemd_dir}/system/default.target.wants
ln -s ../tizen-readahead-collect.service %{buildroot}/%{systemd_dir}/system/default.target.wants/
ln -s ../tizen-readahead-replay.service %{buildroot}/%{systemd_dir}/system/default.target.wants/
mkdir -p %{buildroot}/%{systemd_dir}/system/tizen-boot.target.wants
ln -s ../wm_ready.service %{buildroot}/%{systemd_dir}/system/tizen-boot.target.wants/
mkdir -p %{buildroot}/%{systemd_dir}/system/tizen-system.target.wants

# for host file sharing
mkdir -p %{buildroot}/mnt/host

# include license
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}

%files
/etc/emulator/setup-audio-volume.sh
/etc/emulator/mount-hostdir.sh
/etc/emulator/prerun
/etc/emulator/prerun.d/model-config.sh
/etc/init.d/setup-audio-volume
/etc/init.d/mount-hostdir
/etc/inittab
/etc/preconf.d/emulator_ns.preinit
/etc/preconf.d/systemd_conf.preinit
/etc/profile.d/proxy_setting.sh
/etc/rc.d/rc.emul
/etc/rc.d/rc.firstboot
/etc/rc.d/rc.shutdown
/etc/rc.d/rc.sysinit
/etc/rc.d/rc3.d/S02setup-audio-volume
/etc/rc.d/rc3.d/S03mount-hostdir
/usr/lib/systemd/system/emulator_preinit.target
/usr/lib/systemd/system/emulator.target
/usr/lib/systemd/system/basic.target.wants/emulator_preinit.target
/usr/lib/systemd/system/default.target.wants/tizen-readahead-collect.service
/usr/lib/systemd/system/default.target.wants/tizen-readahead-replay.service
/usr/lib/systemd/system/multi-user.target.wants/emulator.target
/usr/lib/systemd/system/emul-setup-audio-volume.service
/usr/lib/systemd/system/emul-mount-hostdir.service
/usr/lib/systemd/system/emul-common-preinit.service
/usr/lib/systemd/system/dev-vdb.swap
/usr/lib/systemd/system/emulator_preinit.target.wants/emul-setup-audio-volume.service
/usr/lib/systemd/system/emulator_preinit.target.wants/emul-mount-hostdir.service
/usr/lib/systemd/system/emulator_preinit.target.wants/emul-common-preinit.service
/usr/lib/systemd/system/emulator_preinit.target.wants/dev-vdb.swap
/usr/lib/systemd/system/tizen-boot.target.wants/wm_ready.service
/usr/lib/systemd/system/tizen-readahead-collect.service
/usr/lib/systemd/system/tizen-readahead-replay.service
/usr/lib/systemd/system/wm_ready.service
/usr/lib/udev/rules.d/95-tizen-emulator.rules
%dir /mnt/host
/usr/share/license/%{name}
