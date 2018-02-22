import os
from threading import Thread

def updater(m,plugin):
    print('Module %s started' % plugin)
    try:
        func = getattr(m,plugin)()
    except Exception as e:
        print(str(e),plugin)
    print('Module %s completed' % plugin )

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    files = os.listdir('plugins')
    plugins = [plugin for plugin in files if '__' not in plugin]
    plugins = [plugin.replace('.py','') for plugin in plugins if '.pyc' not in plugin]
    for plugin in plugins:
        m = __import__ ('plugins.%s' % (plugin),fromlist=[plugin])
        updater(m,plugin)
        #t = Thread(target=updater, args=(m,plugin,))
        #t.start()
if __name__ == '__main__':
    main()
