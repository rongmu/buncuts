# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os.path as p
from invoke import task, run

base_path = p.dirname(p.realpath(__file__))

# PyInstaller
exe_name = 'BunCuts'

app_file = p.join(base_path, 'app.pyw')
app_icon = p.join(base_path, 'app.ico')

spec_path = base_path
work_path = p.join(base_path, '_build')
dist_path = p.join(base_path, '_dist')

# pyrcc & pyuic
pkg_dir = p.join(base_path, 'buncuts')
res_dir = p.join(pkg_dir, 'res')

res_qrc = p.join(res_dir, 'app.qrc')
res_mod = p.join(pkg_dir, 'app_rc.py')

ui_xml = p.join(res_dir, p.normpath('ui/app.ui'))
ui_mod = p.join(pkg_dir, 'ui.py')


@task
def test():
    """output test"""
    run('echo hello invoke',
        echo=True)


@task
def res():
    """compile resources"""
    run('pyrcc4 -py2 -o "{}" "{}"'.format(res_mod, res_qrc),
        echo=True)


@task
def ui():
    """compile user interface"""
    run('pyuic4 --from-imports --execute -o "{}" "{}"'.format(ui_mod, ui_xml),
        echo=True)


@task
def build():
    """build Windows executable with PyInstaller"""
    run(('pyinstaller --noconsole --onefile '
         '--specpath="{spec}" --workpath="{work}" --distpath="{dist}" '
         '--name={name} --icon="{icon}" "{script}"').format(
             spec=spec_path, work=work_path, dist=dist_path,
             name=exe_name, icon=app_icon, script=app_file),
        echo=True)
