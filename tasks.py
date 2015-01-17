# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os.path
import glob
from invoke import task, run

base_path = os.path.dirname(os.path.realpath(__file__))
pkg_dir = os.path.join(base_path, 'buncuts')
res_dir = os.path.join(pkg_dir, 'res')
ui_pkg = os.path.join(pkg_dir, 'ui')

# PyInstaller
exe_name = 'BunCuts'

app_file = os.path.join(base_path, 'app.pyw')
app_icon = os.path.join(res_dir, os.path.normpath('img/app.ico'))

spec_path = base_path
work_path = os.path.join(base_path, '_build')
dist_path = os.path.join(base_path, '_dist')

clean_paths = (work_path, dist_path,
               os.path.join(spec_path, '{}.spec'.format(exe_name)))

# pyrcc & pyuic
res_name = "app"
res_qrc = os.path.join(res_dir, res_name + '.qrc')
res_mod = os.path.join(ui_pkg, res_name + '_rc.py')
ui_glob = os.path.join(res_dir, os.path.normpath('ui/*.ui'))


@task
def test():
    """output test"""
    run('echo hello invoke',
        echo=True)


@task
def res():
    """compile resources to ui subpackage"""
    run('pyrcc4 -py2 -o "{}" "{}"'.format(res_mod, res_qrc),
        echo=True)


@task
def ui():
    """compile user interface to ui subpackage"""
    for ui_xml in glob.glob(ui_glob):
        name_noext = os.path.splitext(os.path.basename(ui_xml))[0]
        ui_mod = os.path.join(ui_pkg, name_noext + '.py')

        run('pyuic4 --from-imports -o "{}" "{}"'.format(
            ui_mod, ui_xml),
            echo=True)


@task
def app():
    """run the app"""
    run('python {}'.format(app_file),
        echo=True)


@task
def build():
    """build Windows executable with PyInstaller"""
    run(('pyinstaller --noconsole '
         '--specpath="{spec}" --workpath="{work}" --distpath="{dist}" '
         '--name={name} --icon="{icon}" "{script}"').format(
             spec=spec_path, work=work_path, dist=dist_path,
             name=exe_name, icon=app_icon, script=app_file),
        echo=True)


@task
def clean():
    """clean the build files of PyInstaller"""
    for path in clean_paths:
        run('rm -rf "{}"'.format(path),
            echo=True)
