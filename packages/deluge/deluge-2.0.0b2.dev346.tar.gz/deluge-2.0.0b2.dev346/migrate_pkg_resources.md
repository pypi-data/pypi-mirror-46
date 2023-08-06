I am revisiting this problem and a bit rusty with it all so could do with some help.

Firstly how to get a list of packages for a specified path? With `entrypoints` I can hack around to with `iter_files_distros` but with `pkg_resources` it is simpler with

>>> pkg_env = pkg_resources.Environment(['plugins_dir'])
>>> list(pkg_env)
['webui', 'toggle', 'stats', 'scheduler',  'autoadd']
>>> pkg_env['autoadd']
[AutoAdd 1.8 (AutoAdd-1.8-py2.7.egg), AutoAdd 1.7 (AutoAdd-1.7-py2.7.egg), AutoAdd 1.6 (AutoAdd-1.6-py2.7.egg)]

Follow `egg-link` files created from `setup develop --install-dir`? `pkg_resouces` will resolve any egg-links and include them but they are ignored by `entrypoints` (new issue required?). What is the status of egg-links, I know about

Related issue: https://github.com/takluyver/entrypoints/issues/31


Getting the entrypoints is possible but it's not quite matching the existing use-case.

There is a `plugins_dir` directory that the program look in for plugins, wheels, egg, egg folder etc. With pkg_resources it was was possible with `Environment` to search a specified location and it would return all available packages, including multiple versions.

So for an example plugin `AutoAdd` with the following entry_points:

```
entry_points="""
    [deluge.plugin.core]
    AutoAdd = deluge.plugins.autoadd:CorePlugin
    [deluge.plugin.gtk3ui]
    AutoAdd = deluge.plugins.autoadd:Gtk3UIPlugin
    [deluge.plugin.web]
    AutoAdd = deluge.plugins.autoadd:WebUIPlugin
    """
```
```
entry_points={
    "deluge.plugin.core": ["AutoAdd=deluge.plugins.autoadd:CorePlugin"],
    "deluge.plugin.gtk3ui": ["AutoAdd=deluge.plugins.autoadd:Gtk3UIPlugin"],
    "deluge.plugin.web": ["AutoAdd=deluge.plugins.autoadd:WebUIPlugin"]
}
```

Search the plugins directory and find the latest available version:


>>> avail_plugins = [pkg_env[name][0].project_name for name in pkg_env]
>>>
