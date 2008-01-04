%define name	thoggen
%define version	0.6.0
%define release %mkrel 2

Name: 	 	%{name}
Summary: 	Wizard-style DVD backup utility
Version: 	%{version}
Release: 	%{release}

Source:		http://prdownloads.sourceforge.net/thoggen/%{name}-%{version}.tar.bz2
#Patch:		thoggen-0.4.1-new-dvdread.patch.bz2
URL:		http://thoggen.net/
License:	GPL
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	iso-codes
BuildRequires:	libgstreamer-plugins-base-devel
BuildRequires:	libdvdread-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	libhal-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gstreamer0.10-mpeg
BuildRequires:	gstreamer0.10-a52dec gstreamer0.10-mpeg
BuildRequires:	gstreamer0.10-plugins-good
BuildRequires:	gstreamer0.10-plugins-ugly gstreamer0.10-vorbis
BuildRequires:	valgrind
BuildRequires:	perl-XML-Parser
BuildRequires:	desktop-file-utils
Requires:  	gstreamer0.10-a52dec gstreamer0.10-mpeg
Requires:	gstreamer0.10-plugins-good
Requires:  	gstreamer0.10-plugins-ugly gstreamer0.10-vorbis
Requires:	iso-codes
BuildRequires: ImageMagick
ExcludeArch: x86_64

%description
Thoggen is designed to be easy and straight-forward to use. It attempts to
hide the complexity many other transcoding tools expose and tries to offer
sensible defaults that work okay for most people most of the time.
    * Easy to use, with a nice graphical user interface (GUI)
    * Supports title preview, picture cropping, and picture resizing.
    * Language Selection for audio track (no subtitle support yet though)
    * Encodes into Ogg/Theora video
    * Based on the GStreamer multimedia framework, which makes it fairly
      easy to add additional encoding formats/codecs.

%prep
%setup -q
#%patch -p1

%build
%configure2_5x
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rm -fr %buildroot/%_docdir/*
# needed for ABOUT dialog
ln -sf %_docdir/%name-%version %buildroot/%_docdir/%name

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="%{name}" icon="%{name}.png" needs="x11" title="Thoggen" longtitle="DVD backup utility" section="Multimedia/Video" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 data/%name.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 data/%name.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 data/%name.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

pushd .
cd %buildroot%_datadir/locale
mv fr_FR fr
mv pt_PT pt
popd
%find_lang %name
%find_lang %{name}_iso_639
cat %{name}_iso_639.lang >> %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
		
%postun
%clean_menus

%files -f %{name}.lang
%defattr(-,root,root)
# keep COPYING for help files
%doc COPYING README AUTHORS NEWS TODO
%{_bindir}/%name
%{_docdir}/%name
%{_mandir}/man1/*
%{_datadir}/applications/%name.desktop
%{_datadir}/pixmaps/%name.png
%{_datadir}/%name
%{_menudir}/%name
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png


