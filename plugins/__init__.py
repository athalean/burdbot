from .plugins import BurdbotPlugin
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")

# get all names of files in the folder that might contain plugins
ignore_files = ["__init__", "plugins"]
plugin_modules = [ basename(f)[:-3] for f in modules if isfile(f) and basename(f)[:-3] not in ignore_files]


# extract all objects that actually ARE plugins
plugins = []
for mod in plugin_modules:
    plugins.extend(k for k in vars(getattr(__import__("plugins."+mod), mod)).values() if isinstance(k, BurdbotPlugin))

print("Plugins loaded:")
for plugin in plugins:
    if not plugin.author:
        print(" * %s " % plugin.name)
    else:
        print(" * %s by %s" % (plugin.name, plugin.author))
print("")
