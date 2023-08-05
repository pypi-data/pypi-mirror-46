Carrot is a command-line interface for managing Minecraft mods in an MC instance.

It uses an API that indexes all mods and files on CurseForge.

# Installation

## From PyPI

Carrot is published on [PyPI](https://pypi.org/project/carrot-mc/),
therefore the best way to install it is via `pip`:

    pip install carrot-mc

This assumes you're installing it in a virtualenv environment.
If you're installing it globally on Linux, you'll probably need to prepend
the above command with `sudo`.

## From source

You can also download and build your own copy straight from source:

    git clone https://github.com/Misza13/carrot
    cd carrot
    python setup.py install

# Usage

**Important notes:**
 - All commands operate in **the current directory** and assume that you're
   currently in the `mods/` directory of your Minecraft instance.
 - Mods are referred to by their "key", which is the string as it is used
   in CurseForge URLs, e.g. for
   "[Tinkers' Construct](https://minecraft.curseforge.com/projects/tinkers-construct)"
   mod, it's `tinkers-construct`.

To get general help about the program, simply type

    carrot

without any arguments (or just `-h` or `--help`) to see all available commands.

To get help on a specific command, run e.g.

    carrot install -h

Additional pointers on some of the commands follow.

## `init` - initialize the mod repository

Before any usage, you must initialize a mod repository and select the
Minecraft version of this instance, e.g.:

    carrot init --mc_version 1.12.2

This will create a `mods.json` file in the current directory that will hold
information on the installed mods.

Be aware that this will initialize the repository aligned with the `Beta` channel
on CurseForge. To use a different channel, use the `--channel` command, e.g.:

    carrot init --mc_version 1.12.2 --channel Release

The channel determines the stability of mod releases that you wish to receive.
`Beta` is a good default and you may manually override it in other commands
using the same option.

## `install` - install a mod

If you know the exact key of the mod, install it in the current directory using

    carrot install jei

The above example would install the mod "Just Enough Items" because `jei` is
its exact key name. Note that it will use Minecraft version and channel
settings from `mods.json`. The channel can be overridden:

    carrot install jei --channel Release

If there is no mod that matches exactly what you've typed, e.g.

    carrot install applied

you will be presented with a list of top-downloaded mods that have `applied`
in their key (presumably related to Applied Energistics 2 mod).

Stay tuned for a planned `carrot search` command that will allow to search
in names and descriptions of mods.

`install` pulls dependencies, if there are any, e.g.

    carrot install tinkers-construct

will install both Tinkers' Construct itself as well as "Mantle", the
library dependency.

You can also install multiple mods at once by specifying their keys:

    carrot install pams-harvestcraft cooking-for-blockheads

In this mode, Carrot will not display suggestions if keys are not precise,
but instead will simply inform you that the mod was not found and install
only what it can find.

In case of conflicts (e.g. different versions of dependencies either due to
updates or pulling mods from different channels), Carrot will leave already
installed files untouched (to ensure that nothing that already worked breaks),
but you can override this behaviour with `--upgrade` and `--downgrade` flags
(see `carrot install -h` for details). Carrot will verbosely inform you if
this happens, so do pay attention to its output.

## `update` - update mod(-s) to newer/older versions

In its simplest form:

    carrot update

Carrot will attempt to update all currently installed mods (along with their
dependencies) to their newest versions.

Carrot will use the same channel for a mod as the one used to install it,
unless told so otherwise with `--channel`. This means that if, for example,
your entire modpack is set to the `Beta` channel but one mod was installed
explicitly with `--channel Alpha`, that one mod (as well as its dependencies)
will be updated to the latest `Alpha` file but the rest of the mods will use
the default of `Beta`

You can request only a single mod (with dependencies) to be updated with:

    carrot update rftools

Additionally, you can force a target channel with `--channel` option,
which can cause mods to go both up as well as down in versions.
Similarly to `install`, you must explicitly allow `--downgrade` if
you want older versions of mods to be installed. However, unlike
during installation, the equivalent of `--upgrade` is "always on".

## `status` - display status of mod repository

To see a summary of mod installation use:

    carrot status

This will display the following information:
 - Number of mods installed
 - How many of those are dependencies
 - How many mods are disabled (following the `.disabled` convention)
 - List mods whose file is missing (disabled or not)
 - List mods whose file is corrupted (MD5 hash does not match the published one)

## `list` - display list of installed mods

To see the complete list of installed mods use:

    carrot list

This will not only list all mods installed according to `mods.json` but will also
display a status of each:
 - whether file is present or missing,
 - whether it's `.disabled` or not,
 - whether MD5 checksum is correct.

## `enable` and `disable` - enable/disable mods

To enable a mod, use

    carrot enable MOD_KEY

Many mod keys can be specified at the same time, e.g.:

    carrot enable rftools rftools-dimensions

Similarly,

    carrot disable MOD_KEY

will disable a mod (or many mods, if more than one is specified).

Be aware that as of now, dependencies are not disabled/enabled along with the
main mod and have to be toggled manually.

### Enabled/disabled mods

Carrot does not store the enabled/disabled status of mods in `mods.json` and
only looks at the file's name to determine the status. This way, it should be
compatible with other mod managers such as MultiMC which use the standard
convention of disabling mods by appending `.disabled` to their file names.

When installing/updating mods, Carrot will preserve the status, i.e. a disabled
mod will remain disabled after an update and you have to enable it manually.

## `web-gui` - launch a web user interface

To start a web-based interface, simply type:

    carrot web-gui

Carrot comes with an internal webserver that will launch with this command.
By default (that is, unless overridden by the `--host` and `--port` options),
it will listen on http://localhost:8877/ - just point your browser to that
address.

In the `web-gui` you should be able to perform most of the tasks available
purely from the command line. Thus far missing are:
 - `update`
 - `install` with a specific `--channel`

# Future / planned features

## Must-haves for 1.0

 - `search` (in CLI)
 - Uninstall mods (with pruning of unused dependencies)
 - Fix broken mods (missing/corrupted file)
 - Accept directory with mods as parameter instead of always using current
 - Align `web-gui` features with CLI

## After 1.0

 - Manage multiple instances in the Web GUI
   - Copy/paste entire sets of mods between instances
   - Lists of "favourite" sets of mods for easier modpack creation
 - Modpack management - packing/unpacking along with config, resources etc.