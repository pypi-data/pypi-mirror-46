
Freezes Python 3.6+ code into a Windows executable.

There are other projects that do this, but none were an exact fit for something simple.

* Has a simple API that can be used outside of distutils / setuptools.
* Python 3.6 support
* Unlike some maintainers, I actually have Windows

Installing
==========

Kelvin contains two executables which are built from C++ source, so use a binary wheel when
possible::

    pip install kelvin

If you want to build it yourself, install Visual Studio Build Tools 2017.

*Note:* Be sure to choose the Windows 8 SDK in the installer, not the Windows 10 SDK.  The
Windows 10 SDK does not include rc.exe (or it is not in the path), so the linking will fail
with::

    LINK : fatal error LNK1158: cannot run 'rc.exe'


Using
=====

Import the kelvin Builder class and pass the appropriate options to its constructor.  Then call build()::

    from kelvin.builder import Builder

    b = Builder(script='src\\prog.py', dist='dist')
    b.build()

This example creates the executable ``dist\prog.exe`` by analyzing the source for prog.py.

Options
-------

Below are the Builder constructor parameters.  Only ``script``, ``dist``, and ``version`` are
required.

script
  The initial script to start analyzing.  Kelvin will start from this to find dependencies.

dist
  The distribution directory where the executable will be constructed.  If the directory
  exists, all content will be deleted without confirmation!  Make sure this is correct.  If it
  doesn't exist, it will be created.

version
  A string that determines the file version like "1.2.3.4".  Since this is put into the
  executable's version resource, it can only contain numbers and periods.  It cannot contain
  things like "-rc1".  This is a Windows limitation.

  Windows versions always have 4 parts.  If you specify fewer, ".0" will be appended for each
  missing part.

version_strings

  Strings that are also included in the version resource and show up on the "Details" tab of
  the executable's property sheet.  These are provided a dictionary mapping a language id, such
  as 0x0409 for U.S. English, to another dictionary mapping from key to value::

      version_strings = {
          0x0409: {
              'ProductName': 'product',
              'ProductVersion' : '1.2',
              'FileVersion': '1.2.3',
              'FileDescription': 'Descriptiion'
          }
      }

  Note: The FileVersion entry is a string, but it must only contain 1-4 numbers.  If you
  put other things there, it causes the version information to be silently ignored.

filename
  Normally the executable filename is the same as the ``script`` parameter, but a different
  filename can be supplied here.  This should not contain a path - the resulting executable
  will be put into the ``dist`` directory.

subsystem
  Can be 'console' (the default) or 'windows'.  This determines whether the final executable
  is a console application (also used for Windows services) or a GUI application.

path
  Directories that dependencies can be found in, such as library directories.  Kelvin will
  automatically search directories already in ``sys.path``, so I recommend using virtual
  environments to ensure you don't include global items.

include
  A sequence of module names to include, used when modules cannot be identified automatically.
  They can be Python modules or extension modules.

exclude
  Modules to exclude, used when modules are referenced in code but are known to not be needed.
  Kelvin has a large list of exclusions (in analyze.py) for items that are not needed on
  Windows, such as posixpath.  (At this time there is no way to disable the default excludes.)

package_paths
  If you have namespace packages that are split across multiple directories, you'll need to
  pass them here.  Kelvin does not actually run your code, so utilities like
  pkgutils.extend_path won't take effect.

  Provide a dictionary mapping from package name to a sequence of directories::

      package_paths={'mylib': ('lib\\mylib1', 'lib\\mylib2')}

extra
  A sequence of non-code files to be put into the executable.  Each entry can be a relative
  filename, which will be copied into the executable with the same relative name, or a tuple
  pair containing the source path and the path to use in the archive::

      extra = [
          'data\\schema.json',
          ('..\\docs\\README.rst', 'data\\README.rst)
      ]

  This would include the put both files in the executable in a data directory.

  To retrieve these files at runtime, open the executable (``sys.executable``) as a zip file
  using the zipfile package.

logger
  A logging.Logger instance for Kelvin to output to.  If not provided, a logger named "kelvin"
  is used.

  Kelvin outputs very little at the INFO level.  It outputs more at the DEBUG level which may
  be useful for troubleshooting. It also very detailed information at level 1, though this is
  most likely of interest for Kelvin development.  (There is no constant like "TRACE" for this,
  so use ``logger.setLevel(1)``.)


report
  Set to True to have ModuleFinder's report printed to the console.  This can be useful for
  debugging.



How It Works
============

Python's built-in ModuleFinder class is used to analyze your source to find all modules it
uses.

A precompiled executable is copied into the distribution directory.  All needed Python modules
are compiled into a zip file which is appended to the executable.  On startup, the executable
puts itself into ``sys.path`` and Python will load modules from it normally like any other zip
file.  (Interestingly, zip files are processed starting from the end, so we have a zip file
with "garbage" (the executable) at the beginning which is ignored.)

Extension modules are actually DLLs, so they are copied, along with any dependencies, into the
distribution directory, which is also added to ``sys.path``.

This project used to support Python 2.7+, but I am now only supporting Python 3.6+ since it no
longer requires messing with Windows manifest files.  (It is possible that change was made in
Python in 3.5.)  If you need a manifest file, you can either add it after the executable is
complete or you can put it in the same directory as the executable.
