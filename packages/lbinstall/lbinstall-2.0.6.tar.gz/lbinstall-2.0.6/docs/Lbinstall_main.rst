LbInstall
=========

LHCb Package installer

.. image:: https://jenkins-lhcb-core-soft.web.cern.ch/buildStatus/icon?job=Lbinstall
   :target: https://jenkins-lhcb-core-soft.web.cern.ch/job/Lbinstall/


Features
--------

- yum client to select RPMs, with full depenency resolution, using provides/requires as with YUM/RPM
- local install with sqlite DB and filemetadata kept in separate gzipped JSON files
- extract of  the RPMs using the rpmfile python module (patched need to push upstream)
- Run the post install scripts
- checksum verification
- chained install areas / remote databases
- package removal
- package update