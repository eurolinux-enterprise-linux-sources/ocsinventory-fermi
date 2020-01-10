Summary: OCS Inventory NG - Customized for Fermilab
Name: ocsinventory-fermi
Version: 0.9.9
Release: 14
Epoch: 0
License: GPL
Group: System
Source0: %{name}-%{version}.tar.gz
Patch1: ocsinventory-client-slf6.patch
Patch2: ocsinventory-client-ipdiscover.patch
Patch3: ocsinventory-client-cron.patch
URL: http://ocsinventory.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
#kernel-utils is not really needed, but it doesn't gather
#the bios stuff and gives an warning when run
#Requires: kernel-utils
Requires: sed coreutils
Requires: perl-Compress-Zlib perl-XML-Simple perl-XML-Parser perl-URI
Requires: perl-libwww-perl perl-HTML-Parser perl-HTML-Tagset

%description
Open Computer and Software Inventory Next Generation is an 
application designed to help a network or system administrator 
keep track of the computer configuration and software installed 
on the network.

This version has been customized for Fermilab

%prep
%setup -q
%patch1 -p0 
%patch2 -p0 
%patch3 -p0 

%install
mkdir -p %{buildroot}/etc/ocsinventory-client
cp ocsinv.adm %{buildroot}/etc/ocsinventory-client
cp ocsinv.conf %{buildroot}/etc/ocsinventory-client
mkdir -p %{buildroot}/usr/sbin
cp ocsinventory-client.pl %{buildroot}/usr/sbin
#cp ipdiscover %{buildroot}/usr/sbin
mkdir -p %{buildroot}/etc/cron.daily
cp ocs.inventory.client.cron %{buildroot}/etc/cron.daily/z_ocs.inventory.client.cron
mkdir -p %{buildroot}/etc/logrotate.d
cp ocs.logrotate %{buildroot}/etc/logrotate.d/ocs

%clean
rm -rf %{buildroot}

%post
cfile="/etc/ocsinventory-client/ocsinv.conf"
grep -q HOSTNAME.DATE $cfile 2> /dev/null
if [ $? -eq 0 ] ; then
	DEVICENAME=`/bin/uname -n | cut -d . -f1 `
	DEVICEDATE="$(date +%%F-%%k-%%M-%%S)"
	DEVICEID="${DEVICENAME}-${DEVICEDATE}"
	rm -f $cfile.tmp
	cat $cfile | /bin/sed -e "s/HOSTNAME.DATE/${DEVICEID}/" > $cfile.tmp
	mv -f $cfile.tmp $cfile
else
	grep -q heis.fnal.gov $cfile
	if [ $? -eq 0 ] ; then
		cat $cfile | /bin/sed -e "s,<OCSFSERVER>heis.fnal.gov</OCSFSERVER>,<OCSFSERVER>fortytwo.fnal.gov</OCSFSERVER>\n  <XMLLOCALDIR>/etc/ocsinventory-client</XMLLOCALDIR>," > $cfile.tmp
		mv -f $cfile.tmp $cfile		
	fi
fi

%files
%defattr(-, root, root)
%dir /etc/ocsinventory-client
%defattr(0644, root, root)
%config(noreplace) /etc/ocsinventory-client/ocsinv.conf
/etc/ocsinventory-client/ocsinv.adm
/etc/logrotate.d/ocs
%defattr(0755, root, root)
/usr/sbin/ocsinventory-client.pl
#/usr/sbin/ipdiscover
/etc/cron.daily/z_ocs.inventory.client.cron

%changelog
* Thu Dec 8 2011 Connie Sieh <csieh@fnal.gov> 0.9.9-14
- replaced "ifconfig" to "ip addr" in z_ocs.inventory.client.cron
- ifconfig did not work with infiniband

* Mon Dec 27 2010 Troy Dawson <dawson@fnal.gov> 0.9.9-12
- changed the name to ocsinventory-fermi
- Changed PreReq to Requires

* Mon Dec 14 2009 Troy Dawson <dawson@fnal.gov> 0.9.9-11
- Removed ipdiscover from the rpm, removing i386 dependancies

* Mon Jun 15 2009 Connie Sieh <sieh@fnal.gov> 0.9.9-10
- Updated the code to determine $distro and $OSComment for STS and Ubuntu

* Fri Aug 31 2007 Troy Dawson <dawson@fnal.gov> 0.9.9-8
- Added coreutils as a prereq

* Thu Jul 20 2006 Troy Dawson <dawson@fnal.gov> 0.9.9-7
- Updated cron to check to see if it can access the server
  and goes through a list of domains to see if it's at Fermilab

* Fri Jul 13 2006 Troy Dawson <dawson@fnal.gov> 0.9.9-6
- Turned off debugging, check to see if we're on fermilab networks
- Write to a log, and do logrotate
- Minor fixes to the client to now do --local --xml

* Fri Jun 2 2006 Troy Dawson <dawson@fnal.gov> 0.9.9-1
- Client now points to fortytwo as the server
- cronjob now moved to z_... to get a more random time

* Fri Jun 2 2006 Troy Dawson <dawson@fnal.gov> 0.9.8-3
- Client was updated 
- Fixes issues with users using ups perl
- Fixed issue when the rpm comments field has a newline in it.
- Turned debug on the cron job so mail will get sent

* Tue May 30 2006 Troy Dawson <dawson@fnal.gov> 0.9.8-2
- Client was updated 

* Wed May 24 2006 Troy Dawson <dawson@fnal.gov> 0.9.8-1
- Client was updated 
- Cron script was added

* Mon May 15 2006 Troy Dawson <dawson@fnal.gov> 0.9.1-2
- Client was updated 

* Thu Apr 13 2006 Troy Dawson <dawson@fnal.gov> 0.9.1-1
- Updated the client

* Thu Apr 13 2006 Troy Dawson <dawson@fnal.gov> 0.9-3
- Added Requires
- Note that kernel-utils isn't required, but give a 
warning if not installed

* Thu Apr 13 2006 Troy Dawson <dawson@fnal.gov> 0.9-2
- Added ipdiscover

* Thu Apr 13 2006 Troy Dawson <dawson@fnal.gov> 0.9-1
- Initial spec file
