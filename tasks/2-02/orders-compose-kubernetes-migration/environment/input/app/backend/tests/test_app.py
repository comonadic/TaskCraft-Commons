import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('app',Path(__file__).parents[1]/'backend.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_routes():
 assert {'/api/health','/api/orders','/health'}<=set(str(x) for x in m.app.url_map.iter_rules())
