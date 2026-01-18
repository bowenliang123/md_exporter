import os

from dify_plugin import DifyPluginEnv, Plugin

# set system LOAD_FROM_DIFY_PLUGIN to 1 as mark of Dify entry
os.environ["LOAD_FROM_DIFY_PLUGIN"] = "1"

plugin = Plugin(DifyPluginEnv())

if __name__ == "__main__":
    plugin.run()
