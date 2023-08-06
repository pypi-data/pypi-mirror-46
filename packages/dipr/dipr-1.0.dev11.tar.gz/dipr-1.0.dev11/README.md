Dipr (Dipper)
=============

Dipr is a repository management tool meant to provide a revision control independent way of managing dependencies and 
sub-repositories. It is modeled strongly after [guestrepo](https://bitbucket.org/selinc/guestrepo) with numerous
improvements to support multiple revision control systems and additional functionality.

**Dependencies**

A read-only repository that may be pulled and set to a specific revision but should not be modified as part of the
root repo's code base.

**Sub-Repositories**

A living part of the root repository and may change along with the contents of the root repository.  Sub-repositories
may be operated on using the bulk revision control commands below. 

Requirements
============
**Supported OS:**

* Windows
* Linux
* OSX

It has not been tested extensively across multiple revisions of these operating systems.

**Prerequisites:**

* Python >= 3.7
* gitpython >= 2.1
* ruamel-yaml >= 0.15
* git >= 2.0
* hg >= 4.0

Dipr is developed, tested, and built (pyinstaller) in a conda environment.  See [DEVELOPER.md](DEVELOPER.md) for details.

License
=======
Dipr is MIT licensed.  See the [LICENSE.md](LICENSE.md) for details.

Credential Storage
==================

Dipr assumes that credentials are cached as appropriate for the revision control systems that will be used.  Dipr does
no provide any way to specify or store credential information for the dependencies and sub-repositories.  To setup
safe credential caching read some of the following:

**Git:**  [Git Tools Credential Storage](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)

**Mercurial:** [Mercurial Keyring Extension](https://www.mercurial-scm.org/wiki/KeyringExtension)

Implementation of the above may vary depending on platform (Windows, Linux, OSX).  Be sure to read into the various 
options to make sure a secure one is chosen.

Installation
============

It is available via pip:

    > pip install dipr
    
Or using the included setup.py:

    > python setup.py install

Examples
========

General
-------

All the available commands are documented in the built in command line help system:

    > dipr -h
    
Dipr may act upon directories other than the current one:

    > dipr -p "/path/to/the repo" status

Dependency and Sub-Repository Management
----------------------------------------

Initialize the current folder or repo with the dipr YAML files:

    > dipr init

Add some repo sources:
    
    > dipr sources add hg HGDEP1 http://example.com/hg/hgdep1
    > dipr sources add git GITSUB1 http://example.com/git/gitsub1
    > dipr depends add HGDEP1 Depends/HgDep1
    > dipr subrepos add GITSUB1 SubRepos/GitSub1
    
Pull the repos into their folders:

    > dipr pull
    
Update the repos to their specified revisions:
    
    > dipr update

Check the status of the pulled repos:

    > dipr status

Begin development!
    
Import Existing Dependencies or Sub-Repositories
------------------------------------------------

Git submodules:

    > dipr init
    > dipr import submodules --clean
    > dipr pull
    > dipr update
    
Mercurial guestrepos:

    > dipr init
    > dipr import guestrepos --clean
    > dipr pull
    > dipr update

   
Revision Management
-------------------
Bulk revision management is available for both dependencies and sub-repositories.

Freeze repos at their current revision:

    > dipr depends freeze
    
Upgrade repos to their latest tags:

    > dipr depends upgrade --check   
    <... list of available upgrades ...>
    > dipr depends upgrade
    > dipr update
    
Unfreeze repos to their latest revisions in the default branch:

    > dipr depends unfreeze
    > dipr update
    
Set a repo to a specific revision:

    > dipr depends rev --path Depends/HgDep1 --branch DevBranch
    > dipr update
    
Revision Control Commands
-------------------------
Bulk revision control commands can be executed on the root repo (Where .dipr folder is located) and all 
sub-repositories.

Commit root repo and all sub-repositories (adding or removing files as necessary):

    > dipr rcs commit -m "A commit message." --add-remove
    
Tag just the sub-repositories:

    > dipr rcs tag "Release_V1.1.1" -m "A release tag" --exclude-root
    
Push root repo and all sub-repositories to their upstream:

    > dipr rcs push
    
Discard changes in root repo and all sub-repositories:

    > dipr rcs discard
    
Changes in the dependencies may be discarded as well:

    > dipr rcs discard --only-depends
        
Dipr Data Storage
-----------------

All data for dipr is stored in the .dipr directory initialized via the `dipr init` command.  The data files are YAML
formatted and documented with examples of how to add or modify entries manually.

**Sample diprsrc.yaml:**

    DIPSUB1:
        PROTOCOL: GIT
        URL: https://example.com/git/dipsub1.git
  
    HGSUB1:
        PROTOCOL: HG
        URL: https://example.com/hg/hgsub1
        
    DIPDEP1:
        PROTOCOL: GIT
        URL: https://example.com/git/dipdep1.git
        
**Sample diprdep.yaml:**

A repo that will update to a specified tag:

    "Depends/DipDep1":
        KEY: DIPDEP1
        TAG: Release_V1.0.3

A repo that will update to the tip of the default branch:

    "Depends\DiprStuff":
        KEY: DIPRSTUFF

A repo that will update to the tip of DevelBranch:

    "Depends/SubFolder/ODiprStuff":
        KEY: ODIPRTUFF
        BRANCH: DevelBranch

A repo that will update to the specific revision hash:

    "Depends/FinalDiprStuff":
        KEY: FDIPRSTUFF
        REVISION: 234d395
