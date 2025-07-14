Summary:	PC/SC drivers for GemPC 410 and GemPC 430 smart card readers
Summary(pl.UTF-8):	Sterowniki PC/SC do czytników kart procesorowych GemPC 410 i GemPC 430
Name:		pcsc-driver-gempc
Version:	1.0.7
Release:	2
License:	GPL v2+ (GemPC410), BSD (GemPC430)
Group:		Libraries
Source0:	http://ludovic.rousseau.free.fr/softwares/ifd-GemPC/ifd-gempc-%{version}.tar.gz
# Source0-md5:	b15a2ec0cace2523106aab140a38f3e1
Patch0:		%{name}-debug.patch
URL:		http://ludovic.rousseau.free.fr/softwares/ifd-GemPC/index.html
BuildRequires:	libusb-compat-devel
BuildRequires:	pcsc-lite-devel >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PC/SC drivers for GemPC 410 and GemPC 430 smart card readers

%description -l pl.UTF-8
Sterowniki PC/SC do czytników kart GemPC 410 i GemPC 430.

%package serial
Summary:	PC/SC driver for GemPC 410 smart card readers
Summary(pl.UTF-8):	Sterownik PC/SC do czytników kart procesorowych GemPC 410
License:	GPL v2+
Group:		Libraries
Requires:	pcsc-lite >= 1.2.0

%description serial
PC/SC driver for GemPC 410 smart card readers attached through serial
port. Supported hardware:
- GemPC 410: normal GemPC 410, GemPC 410-SL, IBM 410p
- GemPC 412: GCR412 FirstUSA
- GemPC 413: EMV-compliant
- GemPC 415: VISA and American Express 415

Note: GCR400 and GCR410 readers have too old GemCore firmware and are
not supported.

%description serial -l pl.UTF-8
Sterownik PC/SC do czytników kart procesorowych GemPC 410 podłączanych
przez port szeregowy. Obsługiwane czytniki:
- GemPC 410: zwykłe GemPC 410, GemPC 410-SL, IBM 410p
- GemPC 412: GCR412 FirstUSA
- GemPC 413: zgodne z EMV
- GemPC 415: VISA i American Express 415

Uwaga: czytniki GCR400 i GCR410 mają zbyt stare firmware GemCore i nie
są obsługiwane.

%package usb
Summary:	PC/SC driver for GemPC 430 smart card readers
Summary(pl.UTF-8):	Sterownik PC/SC do czytników kart procesorowych GemPC 430
License:	BSD or GPL v2+
Group:		Libraries
Requires:	pcsc-lite >= 1.2.0

%description usb
PC/SC driver for GemPC 430 smart card readers attached through USB
port. Supported hardware:
- GemPC 430: normal GemPC 430
- GemPC 432: target.com
- GemPC 435: American Express Blue Card reader

%description usb -l pl.UTF-8
Sterownik PC/SC do czytników kart procesorowych GemPC 410 podłączanych
przez port USB. Obsługiwane czytniki:
- GemPC 430: zwykłe GemPC 430
- GemPC 432: target.com
- GemPC 435: czytniki American Express Blue Card

%prep
%setup -q -n ifd-gempc-%{version}
%patch -P0 -p1

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -D GemPC410/libGemPC410.so.%{version} $RPM_BUILD_ROOT%{_libdir}/pcsc/drivers/libGemPC410.so
install -d $RPM_BUILD_ROOT/etc/reader.conf.d
cat >$RPM_BUILD_ROOT/etc/reader.conf.d/GemPC410.conf <<EOF
FRIENDLYNAME	"GemPC410"
DEVICEFILE	/dev/ttyS0
LIBPATH		%{_libdir}/pcsc/drivers/libGemPC410.so
CHANNELID	1
EOF

%{__make} -C GemPC430 install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files serial
%defattr(644,root,root,755)
%doc Changelog README README.410 GemPC410/TODO.txt
%attr(755,root,root) %{_libdir}/pcsc/drivers/libGemPC410.so
%config(noreplace) %verify(not md5 mtime size) /etc/reader.conf.d/GemPC410.conf

%files usb
%defattr(644,root,root,755)
%doc Changelog README README.430 GemPC430/{COPYING,TODO.txt}
%dir %{_libdir}/pcsc/drivers/ifd-GemPC430.bundle
%dir %{_libdir}/pcsc/drivers/ifd-GemPC430.bundle/Contents
%{_libdir}/pcsc/drivers/ifd-GemPC430.bundle/Contents/Info.plist
%dir %{_libdir}/pcsc/drivers/ifd-GemPC430.bundle/Contents/Linux
%attr(755,root,root) %{_libdir}/pcsc/drivers/ifd-GemPC430.bundle/Contents/Linux/libGemPC430.so.%{version}
