Usage
=====

Commands
--------

- **query** List packages available in the repositories configured with a name matching the regular expression passed.

::

    lbisnstall [OPTIONS] query [<rpmname regexp>]

Options:
    - **-d, --debug**                       Show debug information
    - **--info**                            Show logging messages with level INFO
    - **--repo=REPOURL**                    Specify repository URL
    - **--nolhcbrepo**                      Do not use the LHCb repositories
    - **--extrarepo=EXTRAREPO**             Specify extra RPM repositories to use
    - **--rpmcache=RPMCACHE**               Specify RPM cache location
    - **--root=SITEROOT**                   Specify MYSITEROOT on the command line
    - **--disable-update-check**            use the YUM metadata in the cache without updating
    - **--disable-yum-check**               use the YUM metadata in the cache without updating
    - **--chained_database=CHAINED_DB**     use a remote database/install area in addition to the local one

- **list** List packages installed on the system matching the regular expression passed.

::

    lbinstall [OPTIONS] list [<rpmname regexp>]

Options:
    - **-d, --debug**                       Show debug information
    - **--info**                            Show logging messages with level INFO
    - **--root=SITEROOT**                   Specify MYSITEROOT on the command line
    - **--chained_database=CHAINED_DB**     use a remote database/install area in addition to the local one

- **check** Verifies is the RPMs are installed correctly on local system.

::

    lbinstall [OPTIONS] check [<rpmname regexp>]

Options:
    - **-d, --debug**                       Show debug information
    - **--info**                            Show logging messages with level INFO
    - **--root=SITEROOT**                   Specify MYSITEROOT on the command line

- **install** Installs a RPM from the yum repository

::

    lbinstall [OPTIONS] install [<rpmname> [<version> [<release>]]

Options:
    - **-d, --debug**                       Show debug information
    - **--info**                            Show logging messages with level INFO
    - **--repo=REPOURL**                    Specify repository URL
    - **--nolhcbrepo**                      Do not use the LHCb repositories
    - **--extrarepo=EXTRAREPO**             Specify extra RPM repositories to use
    - **--rpmcache=RPMCACHE**               Specify RPM cache location
    - **--root=SITEROOT**                   Specify MYSITEROOT on the command line
    - **--dry-run**                         Only print the command that will be run
    - **--just-db**                         Install the packages to the local DB only
    - **--strict**                          Fail if a dependency cannot be resolved
    - **--overwrite**                       Overwrite the files from the package
    - **--disable-update-check**            use the YUM metadata in the cache without updating
    - **--disable-yum-check**               use the YUM metadata in the cache without updating
    - **--nodeps**                          install the package without dependencies
    - **--withdeps**                        update the package with all dependencies. Itworks only on update method
    - **--tmp_dir=TMP_DIR**                 specify a custom tmp directory instead of the default $SITEROOT/tmp
    - **--chained_database=CHAINED_DB**     use a remote database/install area in addition to the local one
    - **--download-pool-size=POOL_SIZE**    the size of the pool thread used to download files

- **remove** Removes a RPM from the local system

::

    lbinstall [OPTIONS] remove [<rpmname> [<version> [<release>]]

Options:
    - **-d, --debug**                       Show debug information
    - **--info**                            Show logging messages with level INFO
    - **--root=SITEROOT**                   Specify MYSITEROOT on the command line
    - **--dry-run**                         Only print the command that will be run
    - **--just-db**                         Install the packages to the local DB only
    - **--strict**                          Fail if a dependency cannot be resolved
    - **--force**                           Force action
    - **--disable-update-check**            use the YUM metadata in the cache without updating
    - **--disable-yum-check**               use the YUM metadata in the cache without updating
    - **--nodeps**                          install the package without dependencies

- **update** Updates a RPM from the yum repository. The rpmname needs to be the same as the one installed on the local system and the version should be grater than the local one, or if equal, the release should be grater.

::

    lbinstall [OPTIONS] update <rpmname> [<version> [<release>]]

Options:
    - **-d, --debug**                       Show debug information
    - **--info**                            Show logging messages with level INFO
    - **--repo=REPOURL**                    Specify repository URL
    - **--nolhcbrepo**                      Do not use the LHCb repositories
    - **--extrarepo=EXTRAREPO**             Specify extra RPM repositories to use
    - **--rpmcache=RPMCACHE**               Specify RPM cache location
    - **--root=SITEROOT**                   Specify MYSITEROOT on the command line
    - **--dry-run**                         Only print the command that will be run
    - **--just-db**                         Install the packages to the local DB only
    - **--strict**                          Fail if a dependency cannot be resolved
    - **--disable-update-check**            use the YUM metadata in the cache without updating
    - **--disable-yum-check**               use the YUM metadata in the cache without updating
    - **--nodeps**                          install the package without dependencies
    - **--withdeps**                        update the package with all dependencies. Itworks only on update method
    - **--tmp_dir=TMP_DIR**                 specify a custom tmp directory instead of the default $SITEROOT/tmp
    - **--chained_database=CHAINED_DB**     use a remote database/install area in addition to the local one
    - **--download-pool-size=POOL_SIZE**    the size of the pool thread used to download files

- **reinstall** Reinstall a RPM from the yum repository. The rpmname, version and release needs to be the same as the one installed on the local system

::

    lbinstall [OPTIONS] reinstall <rpmname> [<version> [<release>]]

Options:
    - **-d, --debug**                       Show debug information
    - **--info**                            Show logging messages with level INFO
    - **--repo=REPOURL**                    Specify repository URL
    - **--nolhcbrepo**                      Do not use the LHCb repositories
    - **--extrarepo=EXTRAREPO**             Specify extra RPM repositories to use
    - **--rpmcache=RPMCACHE**               Specify RPM cache location
    - **--root=SITEROOT**                   Specify MYSITEROOT on the command line
    - **--dry-run**                         Only print the command that will be run
    - **--just-db**                         Install the packages to the local DB only
    - **--strict**                          Fail if a dependency cannot be resolved
    - **--overwrite**                       Overwrite the files from the package
    - **--disable-update-check**            use the YUM metadata in the cache without updating
    - **--disable-yum-check**               use the YUM metadata in the cache without updating
    - **--nodeps**                          install the package without dependencies
    - **--tmp_dir=TMP_DIR**                 specify a custom tmp directory instead of the default $SITEROOT/tmp
    - **--chained_database=CHAINED_DB**     use a remote database/install area in addition to the local one
    - **--download-pool-size=POOL_SIZE**    the size of the pool thread used to download files

- **download** Downloads a RPM from the yum repository

::

    lbinstall [OPTIONS] download <rpmname> [<version> [<release>]]

Options:
    - **-d, --debug**                       Show debug information
    - **--info**                            Show logging messages with level INFO
    - **--repo=REPOURL**                    Specify repository URL
    - **--nolhcbrepo**                      Do not use the LHCb repositories
    - **--extrarepo=EXTRAREPO**             Specify extra RPM repositories to use
    - **--rpmcache=RPMCACHE**               Specify RPM cache location
    - **--root=SITEROOT**                   Specify MYSITEROOT on the command line
    - **--dry-run**                         Only print the command that will be run
    - **--tmp_dir=TMP_DIR**                 specify a custom tmp directory instead of the default $SITEROOT/tmp
    - **--download-pool-size=POOL_SIZE**    the size of the pool thread used to download files

- **graph** Generates a dot file to be used to display the dependencies of a rpm

::

    lbinstall [OPTIONS] graph <rpmname> [<version> [<release>]]

Options:
    - **-d, --debug**                       Show debug information
    - **--info**                            Show logging messages with level INFO
    - **--repo=REPOURL**                    Specify repository URL
    - **--nolhcbrepo**                      Do not use the LHCb repositories
    - **--extrarepo=EXTRAREPO**             Specify extra RPM repositories to use
    - **--rpmcache=RPMCACHE**               Specify RPM cache location
    - **--root=SITEROOT**                   Specify MYSITEROOT on the command line
    - **--tree-mode**                       Used in graph mode to view the graph as a tree instead of a full display
    - **--dot-filename=DOT_FILENAME**       The output filename for dot file. Default is output.dot


Advanced usage
==============

Chaining install areas
----------------------

lbinstall allows creating an install area "chanied" with an existing installation

This allows managing a local area with new packages, not yet deployed to CVMFS for example,
without reinstalling the dependencies already available on that filesystem.

Add a remote (chained) install area
::

    lbinstall --root=$TMPDIR/myroot --chained_database=/cvmfs/lhcb.cern.ch/lib/ install DAVINCI_v42r1_x86_64_slc6_gcc62_opt

If you are using the same root direcotry, you don't need to chaine again the same remote instalation area.


RPM repository selection
-------------------------

lbinstall defaults to the LHCb software repositories, and in normal cases the following options should not be invoked.
However, the configuration can be altered on the command line using the followoing options:

- **--nolhcbrepo**: Clears the configuration. Useless without --extrarepo
- **--extrarepo**: Allows specifying the URL of an extra YUM repository. Can be used several times.
- **--repo**: Changes the common part in the default repository URLs (useful for migrations)

RPM download
----------------

In order to increase the download speed of the RPMs, lbinstall uses a pool of threads to download the files.
The default pool size is 5 threads. The pool size can be increased using:
::

    --download-pool-size=[Number of threads to be used]

Futhuremore, lbinstall has a mode in which it only downloads the rpm files of a given package without installing it.
::

    lbinstall -root=$TMPDIR/myroot download LBSCRIPTS
