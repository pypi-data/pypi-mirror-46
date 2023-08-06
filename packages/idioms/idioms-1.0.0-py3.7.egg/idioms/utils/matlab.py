import re
import os
from munch import Munch

test_str = """
Nfft = 156
a_camel_cased_Arg = 1
scientific_notation = 1e-6
do_matlab_lines_have_semicolons = 1;
% here is a comment!
% more comments
% a comment that has an assignment statement in it
% x = 3
an_alias = scientific_notation;
m
a_derived_variable = Nfft + a_camel_cased_Arg
a_reduced_array = sum(Nfft, a_camel_cased_arg, scientific_notation);
for x in someMatlabObject
    result.x += x
end
    """
boilerplate_end = """        % and yeah that's pretty much that
      catch ME:
          if you_can
              this = some_error_Reporting_stuff
              do_some_more_things(ME)
              goodbye()
              """    
boilerplate_start = """        try
               % boilerplate here
               g = R^arctan(pi)
               for file in some_remote_glob:
                  do_something(file)"""
def extract_atomic_variables(file_contents):
    symbol_table = {}
    body = []
    patt = re.compile(r'\s*([\w_\d]+)+\s*=\s*([\d\-e]+)[;%\s]*')
    for line in file_contents.split("\n"):
       matches = re.match(patt, line)
       if matches:
         sandbox = {}
         try:
            exec(line.strip(), sandbox)
         except Exception as e:
            body.append(line)
         for k,v in sandbox.items():
             if type(v) in (int, complex, float): 
                symbol_table[k] = v
       else:
         body.append(line)     
    body = '\n        '.join(body)
    return Munch({'body': body, 'vars': symbol_table})
     
              
def gen_header(atoms):
    head = "%%%%%% SomeHeaderInitializationKeyword"
    tail = "%%%%%% ThisClosesTheHeader"
    header = [head]
    for k,v in atoms.items():
        header.append(f"%{k} %{v}")
    header.append(tail)
    return '\n'.join(header)

def gen_signature(filepath):
    function_name, _ = os.path.splitext(os.path.basename(filepath))
    function_name = function_name[:-3]
    return f"function {function_name}(inputFile, somethingElse, here_is_an_array_of_butts) {{"

def interpolate_sim_code(filepath="/home/kzeidler/mcc/TestSPRITE_IM.m", sim_code=test_str, boilerplate_start=boilerplate_start, boilerplate_end=boilerplate_end):
    header, extracted_code = gen_header(sim_code)
    sig = gen_signature(filepath)
    body = f"""{header}\n{sig}\n{boilerplate_start}\n{extracted_code}\n{boilerplate_end}
    """
    return body
            
