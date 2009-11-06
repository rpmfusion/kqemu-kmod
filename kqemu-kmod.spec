# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

Name:           kqemu-kmod
Version:        1.4.0
Release:        0.2.pre1%{?dist}.13
Summary:        The QEMU Accelerator Module (KQEMU)

Group:          System Environment/Kernel
License:        GPLv2
URL:            http://www.nongnu.org/qemu/
Source0:        http://www.nongnu.org/qemu/kqemu-%{version}pre1.tar.gz
Source11:       kqemu-kmodtool-excludekernel-filterfile
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  i586 i686 x86_64

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
The QEMU Accelerator Module increases the speed of QEMU when a PC is 
emulated on a PC. It runs most of the target application code directly 
on the host processor to achieve near native performance. 


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%setup -q -c -T -a 0

for kernel_version  in %{?kernel_versions} ; do
    cp -a kqemu-%{version}pre1 _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    pushd _kmod_build_${kernel_version%%___*}
  ./configure \
    --libdir=%{_libdir} \
    --extra-cflags="$RPM_OPT_FLAGS" \
    --kernel-path="${kernel_version##*___}" KERNELRELEASE="${kernel_version%%___*}"
  # jobserver unavailable
  make
popd
done


%install
rm -rf $RPM_BUILD_ROOT
for kernel_version  in %{?kernel_versions} ; do
  mkdir -p $RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
  pushd _kmod_build_${kernel_version%%___*}
    install -D -m 0755 *.ko $RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
  popd
done

%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.13
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.12
- rebuild for new kernels

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.11
- rebuild for new kernels

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.10
- rebuild for new kernels

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.9
- rebuild for final F11 kernel

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.8
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.7
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.6
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.5
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.4
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.3
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.2
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1.1
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.4.0-0.2.pre1
- rebuild for new F11 features

* Thu Mar 12 2009 kwizart < kwizart at gmail.com > - 1.4.0-0.1.pre1
- Update to 1.4.0pre1

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.18
- rebuild for latest Fedora kernel;

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.17
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.16
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.15
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.14
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.13
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.12
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.11
- rebuild for latest Fedora kernel;

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.10
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.9
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.8
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.7
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.6
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.5
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.4
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.3
- rebuild for latest rawhide kernel

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.3.0-0.42.2
- rebuild for latest rawhide kernel

* Sat Oct 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.3.0-0.42.1
- rebuild for rpm fusion

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.3.0-31
- fix typo

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.3.0-30
- build for f9

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.3.0-7
- rebuild for new kmodtools, akmod adjustments

* Wed Jan 09 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.3.0-0.6.pre11
- Integrate patch for 2.6.24
- build akmods package

* Mon Jan  7 2008 kwizart < kwizart at gmail.com > - 1.3.0-0.5.pre11
- Convert to kmod2

* Mon Jan  7 2008 kwizart < kwizart at gmail.com > - 1.3.0-0.4.pre11
- Fix ExclusiveArch: i586 i686 x86_64
- install the module with the right perms

* Sat Jan  5 2008 kwizart < kwizart at gmail.com > - 1.3.0-0.3.pre11
- Some more cleans
- Add ExclusiveArch: i386 x86_64

* Fri Nov  2 2007 kwizart < kwizart at gmail.com > - 1.3.0-0.2.pre11
- Clean for rpmfusion merge

* Fri Feb 09 2007 kwizart < kwizart at gmail.com > - 1.3.0-0.1.pre11
- Initial GPL Release.
