from numpy import mat
from tree_sitter import Language, Parser
import os
from os.path import join as pjoin
import inspect
Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  [
    'tree-sitter-python'
  ]
)
PY_LANGUAGE = Language('build/my-languages.so', 'python')

parser = Parser()
parser.set_language(PY_LANGUAGE)

ROOT='self_contained'
files = os.listdir(ROOT)
files = [f for f in files if f.endswith(".py")]
def parse_assertions(match):
    global function_name
    assert_stm = match[0][0]
    func_stm = match[1][0]
    arg_list = match[2][0]
    returns = match[3][0]
    # print(assert_stm.sexp())
    # print(func_stm.sexp())
    print(arg_list.sexp())
    
    # parse returns
    output={
                "type" : returns.type,
                "value" : returns.text.decode('utf-8'),
                "bytes" : returns.text
            }
    # parse args
    args = []
    if arg_list.text != function_name:
        print('error!')
        exit(1)
    
    
    return {'input':{'args':args},'output':output}

function_name = None

for f in files:
    id = f.split('.')[0].split('_')[-1]
    with open(pjoin(ROOT,f), 'rb') as fp:
        src_lines = fp.read()
    tree = parser.parse(src_lines)
    query = PY_LANGUAGE.query("""
    (function_definition name: (identifier) @function.def
        body:(block
            (expression_statement (string)@docstring)
            (assert_statement
                (comparison_operator
                    (call  function:[
                        (identifier)@func
                    ]
                    arguments:[
                        (argument_list) @args
                    ]
                    )@assert
                    (_)@return
                )
            )            
        )
    )""")
    captures = query.captures(tree.root_node)
    # print(len(captures))
    # for capture in captures:
    #     print(capture[0].sexp())
    #     print(capture[0].text)
    if len(captures) == 0:
        print(f)
        continue
    results = []
    function_name = captures[0][0].text.decode('utf-8').split('_')[-1]
    match_num = int(len(captures)/6)
    captures = captures[2*match_num:]
    raw_matches = [(captures[i],captures[i+1],captures[i+2],captures[i+3]) for i in range(0,len(captures),4)]
    # print(raw_matches)
    for match in raw_matches:
        parse_assertions(match)
        exit(1)
        result = {
            'input':{
                'args':[
                    {
                        'name':match[0].value,
                        'type':match[1].value,
                        'value':match[2].value,
                        "bytes":None
                    }
                ]
            },
            'output':{
                "type" : "int",
                "value" : "",
                "bytes" : None
            }
        }
        # results.append()
    exit(0)