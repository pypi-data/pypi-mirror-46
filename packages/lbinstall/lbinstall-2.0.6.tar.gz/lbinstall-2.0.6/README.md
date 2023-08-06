# LbInstall
[![Build Status](https://jenkins-lhcb-core-soft.web.cern.ch/buildStatus/icon?job=Lbinstall)](https://jenkins-lhcb-core-soft.web.cern.ch/job/Lbinstall/)

LHCb Package installer

## Features

- yum client to select RPMs, with full depenency resolution, using provides/requires as with YUM/RPM
- local install with sqlite DB and filemetadata kept in separate gzipped JSON files
- extract of  the RPMs using the rpmfile python module (patched need to push upstream)
- Run the post install scripts
- checksum verification
- chained install areas / remote databases 
- package removal
- package update


## To try on lxplus


```
virtualenv install
source install/bin/activate
pip install lbinstall
lbinstall --root=$TMPDIR/myroot install DAVINCI_v42r1_x86_64_slc6_gcc62_opt
```

## Commands

- query  : Queries the packages available in the repository
- list   : lists the packages installed locally
- install: Download and install *new* packages
- remove : Remove all files from a local package
- update : Update a package to teh latest version


## Advanced usage


### Chaining install areas

lbinstall allows creating an install area "chanied" with an existing installation: 
this allows managing a local area with new packages, not yet deployed to CVMFS for example, without reinstalling the dependencies already available on that filesystem.

Add a remote (chained) install area
```
lbinstall --root=$TMPDIR/myroot --chained_database=/cvmfs/lhcb.cern.ch/lib/ install DAVINCI_v42r1_x86_64_slc6_gcc62_opt
```
If you are using the same root direcotry, you don't need to chaine again the same remote instalation area. 




### RPM repository selection

lbinstall defaults to the LHCb software repositories, and in normal cases the following options should not be invoked.
However, the configuration can be altered on the command line using the followoing options:

- --nolhcbrepo: Clears the configuration. Useless without --extrarepo
- --extrarepo: Allows specifying the URL of an extra YUM repository. Can be used several times.
- --repo: Changes the common part in the default repository URLs (useful for migrations)

### RPM download

In order to increase the download speed of the RPMs, lbinstall uses a pool of threads to download the files.
The default pool size is 5 threads. The pool size can be increased using:
```
--download-pool-size=[Number of threads to be used]
```
Futhuremore, lbinstall has a mode in which it only downloads the rpm files of a given package without installing it.
```
lbinstall -root=$TMPDIR/myroot download LBSCRIPTS
```

## Design

lbinstall is divided in several components:
- **lbinstall.db.DBManager**: Manages to the local SQLite database containing the list of packages installed
- **lbinstall.db.ChainedDBManager**: Manages to the list of remote installations areas
- **lbinstall.PackageManager**: Module that allows opening RPM files, querying metadat and extracting
- **lbinstall.DependencyManager**: YUM client that queries the inormation from remote repositories
- **lbinstall.InstallAreaManager**: Code to manage the local disk installation and its configuration 
- **lbinstall.Model**: Common classes used to describe RPM packages and their information
- **lbinstall.Installer**: Python installer for the LHCb code
- **lbinstall.LbInstall**: Command line interface to the Installer

Package relationships:

![Package Relationships](doc/packages.png)

Classes relationships:

![Classes Relationships](doc/classes.png)


