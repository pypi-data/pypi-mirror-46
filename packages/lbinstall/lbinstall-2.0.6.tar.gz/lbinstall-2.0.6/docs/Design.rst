Design
======

lbinstall is divided in several components:

- **lbinstall.db.DBManager**: Manages to the local SQLite database containing the list of packages installed
- **lbinstall.db.ChainedDBManager**: Manages to the list of remote installations areas
- **lbinstall.PackageManager**: Module that allows opening RPM files, querying metadat and extracting
- **lbinstall.DependencyManager**: YUM client that queries the inormation from remote repositories
- **lbinstall.InstallAreaManager**: Code to manage the local disk installation and its configuration
- **lbinstall.Model**: Common classes used to describe RPM packages and their information
- **lbinstall.Installer**: Python installer for the LHCb code
- **lbinstall.LbInstall**: Command line interface to the Installer

Package relationships
---------------------

.. image:: ../doc/packages.png
   :target: _images/packages.png

Classes relationships
---------------------
.. image:: ../doc/classes.png
   :target: _images/classes.png

