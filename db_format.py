import ast
import os
from os.path import join as pjoin
import ast
import json

ROOT='self_contained'
ROOT='plib_runnable'
# ROOT='slib_runnable'
files = os.listdir(ROOT)
files = [f for f in files if f.endswith(".py")]
def get_all_funcs_in_file(file_path):
    '''
    Get all the functions defined in one file, include those class methods and standalone functions.
    You can customize the scope of collected functions.
    '''
    try: 
        with open(file_path, 'r') as f:
            file_ast = ast.parse(f.read())
    except:
        print('empty file, exit')
        return []
    # class_defs = [node for node in file_ast.body if isinstance(node, ast.ClassDef)]
    method_defs = []
    # for cls in class_defs:
    #     method_defs.extend([node for node in cls.body if isinstance(node, ast.FunctionDef)])
    function_defs = [node for node in file_ast.body if isinstance(node, ast.FunctionDef)]
    # function_defs.extend(method_defs)
    test_function = None
    focal_function = None
    for func in function_defs:
        if func.name.startswith('test_'):
            test_function = func
    for func in function_defs:
        if func.name==(test_function.name[5:]):
            focal_function = func
    return test_function,focal_function
def generate_json(f):
    global ROOT
    id = f.split('.')[0].split('_')[-1]
    print(f)
    test_func,focal_func = get_all_funcs_in_file(pjoin(ROOT,f))
    focal_doc = ast.get_docstring(focal_func)
    with open(pjoin(ROOT,f), 'r') as fp:
        source_code = fp.readlines()
    test_code = source_code[test_func.lineno-1:test_func.end_lineno]
    test_code = ''.join(test_code)
    focal_code = source_code[focal_func.lineno-1:focal_func.end_lineno]
    focal_code = ''.join(focal_code)
    json_format = {
        'file_path': pjoin(ROOT,f),
        'name': focal_func.name,
        'docstring': focal_doc,
        'lineno': focal_func.lineno,
        'code': focal_code,
        'test_name': test_func.name,
        'test_lineno': test_func.lineno,
        'test_code': test_code,
        'level':ROOT
    }
    return json_format
alls = []
def filter_case(category,f):
    index = f.split('.')[0].split('_')[-1]
    if category=='plib_runnable':
        if index in []:
            return True
    if category=='slib_runnable':
        if index in ['12','3']:
            return True
    return False
cnt = 0        
for f in files:
    
    if not filter_case(ROOT,f):
        corres = generate_json(f)
        alls.append(corres)
        cnt += 1
with open('{}.json'.format(ROOT),'w') as f:
    json.dump(alls,f,indent=4)
print('{} files processed'.format(cnt))
    