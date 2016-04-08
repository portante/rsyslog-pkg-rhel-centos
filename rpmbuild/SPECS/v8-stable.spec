%global _exec_prefix %{nil}
%global _libdir %{_exec_prefix}/%{_lib}
%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog

# Set PIDFILE Variable!
%if 0%{?fedora}0%{?rhel} >= 6
    %define Pidfile syslogd.pid
    %if 0%{?fedora}0%{?rhel} >= 7
    %else
        %define rsysloginit rsyslog.init.epel6
    %endif
    %define rsysloglog rsyslog.log.epel6
%else
    %define Pidfile rsyslogd.pid
    %define rsysloginit rsyslog.init.epel5
    %define rsysloglog rsyslog.log.epel5
%endif

Summary: Enhanced system logging and kernel message trapping daemon
Name: rsyslog
Version: 8.17.0
Release: 1%{?dist}
License: (GPLv3+ and ASL 2.0)
Group: System Environment/Daemons
URL: http://www.rsyslog.com/
Source0: http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1: %{rsysloginit}
Source2: rsyslog_v7.conf
Source3: rsyslog.sysconfig
Source4: %{rsysloglog}
%if %{?rhel} >= 7
# SystemD Patch needed for CentOS 7
#  - tweak the upstream service file to honour configuration from /etc/sysconfig/rsyslog
Patch0: systemd-service.patch
%endif

BuildRequires: autoconf >= 2.52
BuildRequires: automake
BuildRequires: bison
BuildRequires: dos2unix
BuildRequires: flex
BuildRequires: libtool
BuildRequires: libestr-devel >= 0.1.9
BuildRequires: libee-devel
BuildRequires: curl-devel
BuildRequires: libgt-devel
BuildRequires: python-docutils
BuildRequires: liblogging-devel
%if %{?rhel} >= 6
BuildRequires: libfastjson-devel
%else
BuildRequires: json-c-devel
%endif
%if 0%{?fedora}0%{?rhel} >= 7
# make sure systemd is in a version that isn't affected by rhbz#974132
BuildRequires: systemd-devel >= 204-8
%endif
BuildRequires: zlib-devel

Requires: libgt
Requires: logrotate >= 3.5.2
Requires: bash >= 2.0
%if 0%{?fedora}%{?rhel}>= 7
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): /sbin/chkconfig coreutils
Requires(preun): /sbin/chkconfig /sbin/service
Requires(postun): /sbin/service
%endif

Provides: syslog
Obsoletes: sysklogd < 1.5-11
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%package libdbi
Summary: Libdbi database support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libdbi-devel

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mysql-devel >= 4.0

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

%package gssapi
Summary: GSSAPI authentication and encryption support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: krb5-devel

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: librelp >= 1.2.10
BuildRequires: librelp-devel 
BuildRequires: libgcrypt-devel

%package gnutls
Summary: TLS protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: gnutls-devel
BuildRequires: libgcrypt-devel

%package snmp
Summary: SNMP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: net-snmp-devel

%package udpspoof
Summary: Provides the omudpspoof module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libnet-devel

%package mmjsonparse
Summary: JSON enhanced logging support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm1-devel

%package mmnormalize
Summary: Log normalization support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm1-devel

%package mmfields
Summary: mmfields support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: liblognorm1-devel

%package pmaixforwardedfrom
Summary: pmaixforwardedfrom support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmanon
Summary: mmanon support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmutf8fix
Summary: Fix invalid UTF-8 sequences in messages
Group: System Environment/Daemons
Requires: %name = %version-%release

%package ommail
Summary: Mail support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package pmciscoios
Summary: pmciscoios support
Group: System Environment/Daemons
Requires: %name = %version-%release

%if 0%{?fedora}0%{?rhel} >= 6
%package rsgtutil
Summary: RSyslog rsgtutil support
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: %{name}-ksi = %version-%release

%package elasticsearch
Summary: ElasticSearch output module for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libuuid-devel
BuildRequires: libcurl-devel

%package mongodb
Summary: MongoDB output support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libmongo-client-devel

%package kafka
Summary: Kafka output support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: adiscon-librdkafka-devel

%package ksi
Summary: KSI signature support
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: libksi1 >= 3.4.0.0
BuildRequires: libksi1-devel

%package mmgrok
Summary: Grok pattern filtering support
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: grok
BuildRequires: json-c-devel glib2-devel grok grok-devel tokyocabinet-devel
%endif

%description
Rsyslog is an enhanced, multi-threaded syslog daemon. It supports MySQL,
syslog/TCP, RFC 3195, permitted sender lists, filtering on any message part,
and fine grain output format control. It is compatible with stock sysklogd
and can be used as a drop-in replacement. Rsyslog is simple to set up, with
advanced features suitable for enterprise-class, encryption-protected syslog
relay chains.

%description libdbi
This module supports a large number of database systems via
libdbi. Libdbi abstracts the database layer and provides drivers for
many systems. Drivers are available via the libdbi-drivers project.

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

%description gssapi
The rsyslog-gssapi package contains the rsyslog plugins which support GSSAPI
authentication and secure connections. GSSAPI is commonly used for Kerberos
authentication.

%description relp
The rsyslog-relp package contains the rsyslog plugins that provide
the ability to receive syslog messages via the reliable RELP
protocol.

%description gnutls
The rsyslog-gnutls package contains the rsyslog plugins that provide the
ability to receive syslog messages via upcoming syslog-transport-tls
IETF standard protocol.

%description snmp
The rsyslog-snmp package contains the rsyslog plugin that provides the
ability to send syslog messages as SNMPv1 and SNMPv2c traps.

%description udpspoof
This module is similar to the regular UDP forwarder, but permits to
spoof the sender address. Also, it enables to circle through a number
of source ports.

%description mmjsonparse
This module provides support for parsing structured log messages that follow
the CEE/lumberjack specification.

%description mmnormalize
The rsyslog-mmnormalize package provides log normalization by using the
liblognorm and it's Rulebase format.

%description mmfields
Parse all fields of the message into structured data inside the JSON tree.

%description pmaixforwardedfrom
This module cleans up messages forwarded from AIX.
Instead of actually parsing the message, this modifies the message and then
falls through to allow a later parser to handle the now modified message.

%description mmanon
IP Address Anonimization Module (mmanon).
It is a message modification module that actually changes the IP address
inside the message, so after calling mmanon, the original message can
no longer be obtained. Note that anonymization will break digital
signatures on the message, if they exist.

%description mmutf8fix
This module provides support for fixing invalid UTF-8 sequences. Most often,
such invalid sequences result from syslog sources sending in non-UTF character
sets, e.g. ISO 8859. As syslog does not have a way to convey the character
set information, these sequences are not properly handled.

%description pmciscoios
Parser module which supports various Cisco IOS formats.

%description ommail
Mail Output Module.
This module supports sending syslog messages via mail. Each syslog message
is sent via its own mail. The ommail plugin is primarily meant for alerting users.
As such, it is assume that mails will only be sent in an extremely
limited number of cases.

%if 0%{?fedora}0%{?rhel} >= 6
%description rsgtutil
Adds rsyslog utility used for GT and KSI signature verification and more.
For more information see the rsgtutil manual.

%description elasticsearch
This module provides the capability for rsyslog to feed logs directly into
ElasticSearch.

%description mongodb
MongoDB output plugin for rsyslog. This plugin allows rsyslog to write
the syslog messages to MongoDB, a scalable, high-performance,
open source NoSQL database.

%description kafka
librdkafka is a C library implementation of the Apache Kafka protocol,
containing both Producer and Consumer support. It was designed with message delivery
reliability and high performance in mind, current figures exceed 800000 msgs/second
for the producer and 3 million msgs/second for the consumer.

%description ksi
The KSI signature plugin provides access to the Keyless Signature Infrastructure
globally distributed by Guardtime.

%description mmgrok
This module provides filtering based on grok patterns.
%endif

%prep
%setup -q
%if %{?rhel} >= 7
%patch0
%endif

%build
autoreconf -vfi
%ifarch sparc64
#sparc64 need big PIE
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DSYSLOGD_PIDNAME=\\\"%{Pidfile}\\\" -std=c99"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DSYSLOGD_PIDNAME=\\\"%{Pidfile}\\\" -std=c99"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

%configure \
        --disable-generate-man-pages \
        --disable-static \
        --disable-testbench \
%if 0%{?fedora}0%{?rhel} < 6
        --disable-uuid \
%else
        --enable-uuid \
        --enable-elasticsearch \
        --enable-ommongodb \
        --enable-omkafka \
        --enable-usertools \
        --enable-gt-ksi \
    %if 0%{?fedora}0%{?rhel} >= 7
        --enable-imjournal \
        --enable-omjournal \
    %endif
%endif
        --enable-gnutls \
        --enable-imfile \
        --enable-impstats \
        --enable-imptcp \
        --enable-libdbi \
        --enable-mail \
        --enable-mysql \
        --enable-omprog \
        --enable-omudpspoof \
        --enable-omuxsock \
        --enable-pgsql \
        --enable-pmlastmsg \
        --enable-relp \
        --enable-snmp \
        --enable-unlimited-select \
        --enable-mmjsonparse \
        --enable-mmnormalize \
        --enable-mmanon \
        --enable-mmutf8fix \
        --enable-mail \
        --enable-mmfields \
        --enable-mmpstrucdata \
        --enable-mmsequence \
        --enable-pmaixforwardedfrom \
        --enable-pmciscoios \
        --enable-guardtime \
        --enable-mmgrok \
        --enable-gssapi-krb5

make V=1

%install
rm -rf %{buildroot}

make V=1 DESTDIR=%{buildroot} install

%if 0%{?fedora}0%{?rhel} <= 6
install -d -m 755 %{buildroot}%{_initrddir}
%endif
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -d -m 755 %{buildroot}%{_sysconfdir}/rsyslog.d
install -d -m 700 %{buildroot}%{rsyslog_statedir}
install -d -m 700 %{buildroot}%{rsyslog_pkidir}

%if 0%{?fedora}0%{?rhel} <= 6
install -p -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/rsyslog
%endif
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rsyslog.conf
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/rsyslog
install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/syslog

# get rid of libtool libraries
rm -f %{buildroot}%{_libdir}/rsyslog/*.la

%clean
rm -rf %{buildroot}

%post
%if 0%{?fedora}0%{?rhel} <= 6
/sbin/chkconfig --add rsyslog
%endif
for n in /var/log/{messages,secure,maillog,spooler}
do
    [ -f $n ] && continue
    umask 066 && touch $n
done
%if 0%{?fedora}0%{?rhel} >= 7
%systemd_post rsyslog.service
%endif

%preun
%if 0%{?fedora}0%{?rhel} <= 6
if [ $1 = 0 ]; then
    service rsyslog stop >/dev/null 2>&1 ||:
    /sbin/chkconfig --del rsyslog
fi
%else
%systemd_preun rsyslog.service
%endif

%postun
%if 0%{?fedora}0%{?rhel} <= 6
if [ "$1" -ge "1" ]; then
    service rsyslog condrestart > /dev/null 2>&1 ||:
fi
%else
%systemd_postun_with_restart rsyslog.service
%endif

%triggerun -- rsyslog < 5.7.8-1
## Save the current service runlevel info
## User must manually run systemd-sysv-convert --apply rsyslog
## to migrate them to systemd targets
#%{_bindir}/systemd-sysv-convert --save rsyslog >/dev/null 2>&1 || :
#/bin/systemctl enable rsyslog.service >/dev/null 2>&1 || :
#/sbin/chkconfig --del rsyslog >/dev/null 2>&1 || :
#/bin/systemctl try-restart rsyslog.service >/dev/null 2>&1 || :
# previous versions used a different lock file, which would break condrestart
[ -f /var/lock/subsys/rsyslogd ] || exit 0
mv /var/lock/subsys/rsyslogd /var/lock/subsys/rsyslog
[ -f /var/run/rklogd.pid ] || exit 0
/bin/kill `cat /var/run/rklogd.pid 2> /dev/null` > /dev/null 2>&1 ||:

#%triggerpostun -n rsyslog-sysvinit -- rsyslog < 5.8.2-3
#/sbin/chkconfig --add rsyslog >/dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* NEWS ChangeLog README.md
%dir %{_libdir}/rsyslog
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/imklog.so
%{_libdir}/rsyslog/immark.so
%{_libdir}/rsyslog/impstats.so
%{_libdir}/rsyslog/imptcp.so
%{_libdir}/rsyslog/imtcp.so
%{_libdir}/rsyslog/imudp.so
%{_libdir}/rsyslog/lmnet.so
%{_libdir}/rsyslog/imuxsock.so
%{_libdir}/rsyslog/lmnetstrms.so
%{_libdir}/rsyslog/lmnsd_ptcp.so
%{_libdir}/rsyslog/lmregexp.so
%{_libdir}/rsyslog/lmstrmsrv.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omprog.so
%{_libdir}/rsyslog/omuxsock.so
%{_libdir}/rsyslog/pmlastmsg.so
%{_libdir}/rsyslog/lmcry_gcry.so
%{_libdir}/rsyslog/lmsig_gt.so
%{_libdir}/rsyslog/mmpstrucdata.so
%{_libdir}/rsyslog/mmsequence.so
%{_libdir}/rsyslog/mmexternal.so
%if 0%{?fedora}0%{?rhel} >= 7
%{_libdir}/rsyslog/imjournal.so
%{_libdir}/rsyslog/omjournal.so
%endif
%if 0%{?fedora}0%{?rhel} >= 6
%{_bindir}/rscryutil
%endif
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
%dir %{_sysconfdir}/rsyslog.d
%dir %{rsyslog_statedir}
%dir %{rsyslog_pkidir}
%if 0%{?fedora}0%{?rhel} <= 6
%{_initrddir}/rsyslog
%endif
%{_sbindir}/rsyslogd
%{_mandir}/*/*
%if 0%{?fedora}0%{?rhel} >= 7
%{_unitdir}/rsyslog.service
%endif

%files libdbi
%defattr(-,root,root)
%{_libdir}/rsyslog/omlibdbi.so

%files mysql
%defattr(-,root,root)
%doc plugins/ommysql/createDB.sql
%{_libdir}/rsyslog/ommysql.so

%files pgsql
%defattr(-,root,root)
%doc plugins/ompgsql/createDB.sql
%{_libdir}/rsyslog/ompgsql.so

%files gssapi
%defattr(-,root,root)
%{_libdir}/rsyslog/lmgssutil.so
%{_libdir}/rsyslog/imgssapi.so
%{_libdir}/rsyslog/omgssapi.so

%files relp
%defattr(-,root,root)
%{_libdir}/rsyslog/imrelp.so
%{_libdir}/rsyslog/omrelp.so

%files gnutls
%defattr(-,root,root)
%{_libdir}/rsyslog/lmnsd_gtls.so

%files snmp
%defattr(-,root,root)
%{_libdir}/rsyslog/omsnmp.so

%files udpspoof
%defattr(-,root,root)
%{_libdir}/rsyslog/omudpspoof.so

%files mmjsonparse
%defattr(-,root,root)
%{_libdir}/rsyslog/mmjsonparse.so

%files mmnormalize
%defattr(-,root,root)
%{_libdir}/rsyslog/mmnormalize.so

%files mmfields
%defattr(-,root,root)
%{_libdir}/rsyslog/mmfields.so

%files pmaixforwardedfrom
%defattr(-,root,root)
%{_libdir}/rsyslog/pmaixforwardedfrom.so

%files mmanon
%defattr(-,root,root)
%{_libdir}/rsyslog/mmanon.so

%files pmciscoios
%defattr(-,root,root)
%{_libdir}/rsyslog/pmciscoios.so

%files mmutf8fix
%defattr(-,root,root)
%{_libdir}/rsyslog/mmutf8fix.so

%files ommail
%defattr(-,root,root)
%{_libdir}/rsyslog/ommail.so

%if 0%{?fedora}0%{?rhel} >= 6
%files rsgtutil
%defattr(-,root,root)
%{_bindir}/rsgtutil

%files elasticsearch
%defattr(-,root,root)
%{_libdir}/rsyslog/omelasticsearch.so

%files mongodb
%defattr(-,root,root)
%{_libdir}/rsyslog/ommongodb.so
%if 0%{?fedora}0%{?rhel} >= 6
%{_bindir}/logctl
%endif

%files kafka
%defattr(-,root,root)
%{_libdir}/rsyslog/omkafka.so

%files ksi
%defattr(-,root,root)
%{_libdir}/rsyslog/lmsig_ksi.so

%files mmgrok
%defattr(-,root,root)
%{_libdir}/rsyslog/mmgrok.so
%endif


%changelog
* Wed Mar 23 2016 Peter Portante
- Merge with Fedora's spec file
- Enable mmgrok

* Tue Mar 08 2016 Florian Riedl
- Updated RPM's for Rsyslog 8.17.0

* Wed Feb 10 2016 Andre Lorbach
- Added systemd patch for CentOS7

* Tue Feb 09 2016 Florian Riedl
- Fixed libksi dependency

* Tue Jan 26 2016 Florian Riedl
- Updated RPM's for Rsyslog 8.16.0

* Fri Dec 18 2015 Florian Riedl
- Updated RPM's for Rsyslog 8.15.0

* Thu Dec 10 2015 Andre Lorbach
- KSI signature support has to be moved from
  the base package to rsyslog-ksi
- Moved rsgtutil into own package.

* Tue Nov 03 2015 Florian Riedl
- Updated RPM's for Rsyslog 8.14.0
- added imjournal and omjournal to base RPM

* Tue Sep 22 2015 Florian Riedl
- Updated RPM's for Rsyslog 8.13.0

* Tue Aug 11 2015 Florian Riedl
- Updated RPM's for Rsyslog 8.12.0

* Tue Jul 14 2015 Florian Riedl
- Updated RPM's to use librdkafka 0.8.6

* Tue Jun 30 2015 Florian Riedl
- Updated RPM's for Rsyslog 8.11.0
- Added GT KSI support

* Tue Jun 09 2015 Florian Riedl
- Updated RPM's for Rsyslog 8.10.0.ad1

* Fri May 29 2015 Andre Lorbach
- Created RPM's for Rsyslog 8.10.0.ad1

* Tue May 19 2015 Florian Riedl
- Created RPM's for Rsyslog 8.10.0

* Thu Apr 23 2015 Florian Riedl
- Created RPM's for Rsyslog 8.9.0.ad1

* Thu Apr 09 2015 Florian Riedl
- Created RPM's for Rsyslog 8.9.0 for RHEL5

* Tue Apr 07 2015 Florian Riedl
- Created RPM's for Rsyslog 8.9.0

* Tue Mar 17 2015 Florian Riedl
- Updated RPM's for Rsyslog 8.8.0.ad1 to include omkafka

* Thu Mar 12 2015 Florian Riedl
- Updated RPM's for Rsyslog 8.8.0.ad1 to support liblognorm 1.1.1

* Thu Mar 05 2015 Florian Riedl
- Created RPM's for Rsyslog 8.8.0.ad1

* Wed Feb 25 2015 Andre Lorbach
- Created RPM's for Rsyslog 8.8.0

* Tue Jan 13 2015 Florian Riedl
- Created RPM's for Rsyslog 8.7.0

* Tue Dec 02 2014 Florian Riedl
- re-release of 8.6.0

* Mon Dec 01 2014 Florian Riedl
- Created RPM's for RSyslog 8.6.0

* Wed Nov 12 2014 Florian Riedl
- Created RPM's for RSyslog 8.4.2.ad1

* Tue Nov 04 2014 Andre Lorbach
- Added pmaixforwardedfrom module

* Thu Oct 02 2014 Andre Lorbach
- Created RPM's for RSyslog 8.4.2

* Wed Oct 01 2014 Florian Riedl
- fixed GPG signing

* Tue Sep 30 2014 Florian Riedl
- Created RPM's for RSyslog 8.4.1

* Mon Aug 18 2014 Andre Lorbach
- Created RPM's for RSyslog 8.4.0

* Thu Jun 26 2014 Andre Lorbach
- Created RPM's for RSyslog 8.2.2

* Sat Jun 14 2014 Mike Liebsch
- Added mmutf8fix support
- Updated to RSyslog 8.2.2

* Tue Apr 22 2014 Andre Lorbach
- Created RPM's for RSyslog 8.2.1

* Wed Apr 02 2014 Andre Lorbach
- Final Build for first V8-Stable release

* Tue Apr 01 2014 Andre Lorbach
- First Testbuild for RSyslog V8-Stable

* Tue Mar 11 2014 Andre Lorbach
- New build for librelp

* Fri Mar 07 2014 Andre Lorbach
- new build for CentOS 6

* Thu Feb 20 2014 Andre Lorbach
- Created RPM's for RSyslog 8.1.6

* Fri Jan 24 2014 Andre Lorbach
- Created RPM's for RSyslog 8.1.5

* Fri Jan 10 2014 Andre Lorbach
- Created RPM's for RSyslog 8.1.4

* Fri Dec 06 2013 Andre Lorbach
- Created RPM's for RSyslog 8.1.3

* Thu Nov 28 2013 Andre Lorbach
- Created RPM's for RSyslog 8.1.2
  Added jemalloc support

* Tue Nov 19 2013 Andre Lorbach
- Created RPM's for RSyslog 8.1.1

* Fri Nov 15 2013 Andre Lorbach
- Created RPM's for RSyslog 8.1.0

* Thu Nov 07 2013 Andre Lorbach
- Removed unused reload option
  from INIT script.

* Wed Oct 30 2013 Andre Lorbach
- Added mmsequence modul into base package

* Tue Oct 29 2013 Andre Lorbach
- Created RPM's for RSyslog 7.5.6

* Tue Oct 15 2013 Andre Lorbach
- Created RPM's for RSyslog 7.5.5

* Mon Oct 07 2013 Andre Lorbach
- Created RPM's for RSyslog 7.5.4

* Wed Sep 11 2013 Andre Lorbach
- Added RPM Package for mmfields
- Created RPM's for RSyslog 7.5.3

* Thu Jul 04 2013 Andre Lorbach
- Created RPM's for RSyslog 7.5.2

* Wed Jun 26 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.5.1

* Tue Jun 11 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.5.0

* Tue May 21 2013 Andre Lorbach
- Added new module ommail

* Wed May 15 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.15

* Wed May 08 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.14

* Thu Apr 25 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.12

* Sat Apr 13 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.10

* Thu Mar 28 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.9

* Fri Mar 22 2013 Andre Lorbach
- Testing RPMs for v7-devel 7.3.9

* Mon Mar 18 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.8

* Thu Mar 14 2013 Andre Lorbach
- Added RPM Package for mmanon

* Wed Mar 13 2013 Andre Lorbach
- Created new RPMs for v7-devel 7.3.7

* Tue Mar 12 2013 Andre Lorbach
- Added RPM Package for mmnormalize

* Fri Mar 08 2013 Andre Lorbach
- Added RPM Package for MongoDB

* Fri Feb 22 2013 Andre Lorbach
- removed -c option from sysconfig file

* Tue Jan 29 2013 Andre Lorbach
- Added new default configuration which is only
  V7 compatible.
- Created new RPMs for v7-devel 7.3.6

* Thu Jan 17 2013 Andre Lorbach
- Added Module for omelasticsearch ,
  thanks to Radu Gheorghe. Support is only available on
  EHEL 6 and higher!
- Added Module for mmjsonparse.

* Wed Dec 19 2012 Andre Lorbach
- Created new RPMs for v7-devel 7.3.5

* Wed Nov 21 2012 Andre Lorbach
- Changed PIDFile back to rsyslog.pid for EPEL5 dist
- removed depencies for libuuid-devel package

* Wed Nov 07 2012 Andre Lorbach
- Created RPMs for v7-devel: 7.3.3

* Fri Oct 19 2012 Andre Lorbach
- Created Specfile and RPMs for v7-devel: 7.3.1

* Wed Oct 17 2012 Andre Lorbach
- created RPMs for RSyslog 7.1.11

* Mon Oct 15 2012 Andre Lorbach
- removed systemd-units dependency

* Thu Sep 06 2012 Andre Lorbach
- created RPMs for RSyslog 7.1.0

* Fri Aug 24 2012 Andre Lorbach
- Adapted RPM Specfile for RSyslog 6 and 7

* Thu Aug 23 2012 Andre Lorbach
- created RPMs for 5.8.13, no changes needed
