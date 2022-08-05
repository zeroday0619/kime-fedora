Summary:		KIME 한글입력기 
Name:			kime
Version:		2.5.6
Release:		1%{?dist}
Group:			System/Internalization
Vendor:			zeroday0619
License:		GPLv3
URL:			https://github.com/Riey/kime/
Source0:		%{name}-v%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-root
BuildArch:		x86_64
BuildRequires:	llvm-devel
BuildRequires:	rust
BuildRequires:	cargo
BuildRequires:  cmake
BuildRequires:  libappindicator-devel
BuildRequires:  clang
BuildRequires:  clang-libs
BuildRequires:  clang-devel
BuildRequires:	cairo
BuildRequires:  cairo-devel
BuildRequires:  cairo-gobject
BuildRequires:  cairo-gobject-devel
BuildRequires:  gtk3-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  desktop-file-utils

%define kime_conf_dir /etc/xdg/%{name}
%define kime_inc_dir %{_includedir}
%define kime_lib_dir %{_libdir}
%define kime_gtk2_dir %{_libdir}/gtk-2.0/2.10.0/immodules
%define kime_gtk3_dir %{_libdir}/gtk-3.0/3.0.0/immodules
%define kime_qt5_dir %{_libdir}/qt5/plugins/platforminputcontexts
%define kime_icons_dir %{_datadir}/%{name}/icons
%define kime_build_dir build/out

%description

GTK및 QT5 대부분 프로그램에서 한글을 입력할 수 있는 새로운 한글 입력기

%prep

%setup

%build
scripts/build.sh -ar

%install
rm -rf %{buildroot}
install -d -p  %{buildroot}%{_bindir}
install -d -p  %{buildroot}%{kime_qt5_dir}
install -d -p  %{buildroot}%{kime_gtk2_dir}
install -d -p  %{buildroot}%{kime_gtk3_dir}
install -d -p  %{buildroot}%{kime_inc_dir}
install -d -p  %{buildroot}%{kime_icons_dir}
install -d -p  %{buildroot}%{kime_conf_dir}
install -d -p  %{buildroot}%{_datadir}/im-config/data

install -Dm 0755 %{kime_build_dir}/kime-* %{buildroot}%{_bindir}
install -Dm 0755 %{kime_build_dir}/libkime-gtk2.so %{buildroot}%{kime_gtk2_dir}/im-kime.so
install -Dm 0755 %{kime_build_dir}/libkime-gtk3.so %{buildroot}%{kime_gtk3_dir}/im-kime.so
install -Dm 0755 %{kime_build_dir}/libkime-qt5.so %{buildroot}%{kime_qt5_dir}/libkimeplatforminputcontextplugin.so
install -Dm 0755 %{kime_build_dir}/libkime_engine.so %{buildroot}%{_libdir}/
install -Dm 0644 %{kime_build_dir}/icons/*/* %{buildroot}%{kime_icons_dir}/
install -Dm 0644 %{kime_build_dir}/default_config.yaml %{buildroot}%{kime_conf_dir}/config.yaml
install -Dm 0644 %{kime_build_dir}/kime_engine.hpp %{buildroot}%{kime_inc_dir}
install -Dm 0644 %{kime_build_dir}/kime_engine.h %{buildroot}%{kime_inc_dir}
install -Dm 0644 %{kime_build_dir}/LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE

install -d -p  %{buildroot}%{_desktopdir}

cat << EOF > %{buildroot}%{_desktopdir}/kime-indicator.desktop
[Desktop Entry]
Name=kime-indicator
Comment=kime 한글입력기 표시기
StartupNotify=true
Terminal=false
Type=Application
Icon=//usr/share/kime/icons/kime-han-64x64.png
Exec=/usr/bin/kime-indicator
Categories=X-MandrivaLinux-MoreApplications-Configuration
EOF

desktop-file-install --vendor "" \
		    --dir %{buildroot}%{_desktopdir} %{buildroot}%{_desktopdir}/kime-indicator.desktop
		    
%clean
rm -rf %{buildroot}

%post
gtk-query-immodules-2.0 --update-cache
gtk-query-immodules-3.0-64 --update-cache
cp %{_desktopdir}/kime-indicator.desktop /home/$USER/Desktop
chown $USER.$USER /home/$USER/Desktop/kime-indicator.desktop

mv /home/$USER/.i18n /home/$USER/.i18n.old

cat > /home/$USER/.i18n <<EOF
CONSOLE_NOT_LOCALIZED=yes
ENC=utf8
LANG=ko_KR.UTF-8
LANGUAGE=ko_KR.UTF-8:ko
LC_ADDRESS=ko_KR.UTF-8
LC_COLLATE=ko_KR.UTF-8
LC_CTYPE=ko_KR.UTF-8
LC_IDENTIFICATION=ko_KR.UTF-8
LC_MEASUREMENT=ko_KR.UTF-8
LC_MESSAGES=ko_KR.UTF-8
LC_MONETARY=ko_KR.UTF-8
LC_NAME=ko_KR.UTF-8
LC_NUMERIC=ko_KR.UTF-8
LC_PAPER=ko_KR.UTF-8
LC_TELEPHONE=ko_KR.UTF-8
LC_TIME=ko_KR.UTF-8
GTK_IM_MODULE=kime
QT_IM_MODULE=kime
XMODIFIERS=@im=kime
XIM_PROGRAM=kime-xim
EOF

%postun
gtk-query-immodules-2.0 --update-cache
gtk-query-immodules-3.0-64 --update-cache
rm -f /home/$USER/Desktop/kime-indicator.desktop
rm -f /home/$USER/.i18n
mv /home/$USER/.i18n.old /home/$USER/.i18n

%files


%defattr(-,root,root) 
%doc LICENSE
%{_bindir}/*
%{_desktopdir}/kime-indicator.desktop
%{kime_icons_dir}/*
%{kime_conf_dir}/config.yaml
%{kime_gtk2_dir}/im-kime.so
%{kime_gtk3_dir}/im-kime.so
%{kime_qt5_dir}/libkimeplatforminputcontextplugin.so
%{_libdir}/libkime_engine.so
%{_includedir}/kime*

%changelog
* Tue Jun 28 2022 zeroday0619 2.5.6-1
- write auto build script

* Tue Feb 16 2021 dumca - 1.0.3-5
- fix spec file

* Tue Feb 16 2021 dumca - 1.0.3-4
- fix icons dir

* Mon Feb 15 2021 dumca - 1.0.3-3
- updated gtk-query-immodules caching
- support GTK 

* Mon Feb 15 2021 dumca - 1.0.3-2
- updated
- fix package

* Mon Feb 15 2021 dumca - 1.0.2-1
- new build


