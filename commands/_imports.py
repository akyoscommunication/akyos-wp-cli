from commands.help import help_cmd as _help_cmd
global help_cmd
help_cmd = _help_cmd

from commands.component.create import create_cmd as _create_cmd
global create_cmd
create_cmd = _create_cmd
from commands.component._import import import_cmd as _import_cmd
global import_cmd
import_cmd = _import_cmd
from commands.component.export import export_cmd as _export_cmd
global export_cmd
export_cmd = _export_cmd

from commands.project.install import install_cmd as _install_cmd
global install_cmd
install_cmd = _install_cmd
from commands.project.serve import serve_cmd as _serve_cmd
global serve_cmd
serve_cmd = _serve_cmd
from commands.project.build import build_cmd as _build_cmd
global build_cmd
build_cmd = _build_cmd
from commands.project.push import push_cmd as _push_cmd
global push_cmd
push_cmd = _push_cmd
from commands.project.create import createproject_cmd as _createproject_cmd
global createproject_cmd
createproject_cmd = _createproject_cmd

from commands.database.replace import replace_cmd as _replace_cmd
global replace_cmd
replace_cmd = _replace_cmd
from commands.database._import import dbimport_cmd as _dbimport_cmd
global dbimport_cmd
dbimport_cmd = _dbimport_cmd
from commands.database.dump import dump_cmd as _dump_cmd
global dump_cmd
dump_cmd = _dump_cmd

from commands.test import test_cmd as _test_cmd
global test_cmd
test_cmd = _test_cmd
from commands.doctor import doctor_cmd as _doctor_cmd
global doctor_cmd
doctor_cmd = _doctor_cmd
from commands.update import update_cmd as _update_cmd
global update_cmd
update_cmd = _update_cmd
