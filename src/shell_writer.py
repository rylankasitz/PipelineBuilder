import os
import json_loader
import textwrap

# SBATCH
SBATCH_COMMENT = '#SBATCH '
SBATCH = 'SBATCH '
BINBASH = '#!/bin/bash'

# Commands
MKDIR = 'mkdir '
TOUCH = 'touch '
EXPORT = 'export '
SHIFT = 'shift'
REMOVE = 'rm '
SLEEP = 'sleep '
LIST = 'ls '
WC = 'wc '

# Formatting
TAB = '\t'
NEW_LINE = '\n'
EMPTY_STATMENT = ''

# File Writers
def write(file_, contents):
    f = open(file_, "w+")
    f.write(contents)
    f.close()
 
# Main Writers   
def pipeline(workspace, shell_args_, cmd_args, steps):
    step_location = _ref(workspace) + '/.steps'
    uuid_file = _extention(step_location + '/' + _ref('uuid'), 'done')
    step_count = len(steps) + 1
    
    pipeline_step_statements = ([REMOVE + uuid_file] + 
                               [(_if_statement(_cond(_equal(_ref('step'), _quote('0'))), 
                                               step)) for step in steps] +
                               [_increment('step')])
    
    inner_while_statements = [_assignment('file', uuid_file),
                              _if_statement(_cond(_arg('f', shorthand=True) + ' ' + _ref('file')), 
                                           _statements(pipeline_step_statements)),
                              _sleep(30)]
    
    return _statements([shell_args(shell_args_),
                        EMPTY_STATMENT,
                        commandline_args(cmd_args),
                        EMPTY_STATMENT,
                        _assignment('step', '0'), 
                        _assignment('uuid', _quote('init')), 
                        make_directory(step_location), 
                        touch_file(uuid_file),
                        EMPTY_STATMENT,
                        _while_loop(_cond(_less_than(_ref('steps'), _quote(step_count))), 
                                   _statements(inner_while_statements))])
    
def loop(workspace, loop_directory, mapping, command):
    done_count = _ref('(' + pipe_command(LIST + _arg('lR', shorthand=True) + ' ' 
                                               + _extention(_ref(loop_directory + '/../*'), 'done'), 
                                          WC + _arg('l', shorthand=True))
                      + ')')
    done_file = _extention(workspace + '/.steps/uuid', 'done')
    return _statements([_assignment('counter', 0),
                        EMPTY_STATMENT,
                       _for_loop(loop_directory + '/' + mapping, 
                                 _statements([command, _increment('counter')])),
                       EMPTY_STATMENT,
                       _while_loop(_cond(_less_than(done_count, _ref('counter'))),
                                   _sleep(30)),
                       EMPTY_STATMENT,
                       touch_file(done_file),
                       remove_file(done_file),
                       _assignment('uuid', _quote('loop'))
                       ])

def program(workspace, _file, inputs, outputs):
    return _statements([SBATCH + _file + ' ' + 
                     ' '.join([_arg(name, shorthand=False) + ' ' + arg 
                               for name, arg in inputs.items()]) + ' ' + 
                     ' '.join([_arg(name, shorthand=False) + ' ' + _ref(workspace) + '/' + arg 
                               for name, arg in outputs.items()])])

def program_wrapper(s_args, cmd_args, command):
    return _statements([shell_args(s_args), 
                        EMPTY_STATMENT,
                        commandline_args(cmd_args), 
                        EMPTY_STATMENT,
                        command,
                        EMPTY_STATMENT,
                        touch_file(_ref('done'))])
    

# Statement Writers
def commandline_args(cmd_args):
    cases = {}
    for arg in cmd_args:
        cases[_arg(arg)] = _statements([SHIFT, _assignment(arg, _ref('1'))])
    return _while_loop(_cond(_not_equal(_ref('1'), _quote(''))), 
                       _statements([_case_statement(_ref('1'), cases), 
                                    SHIFT]))
    
def shell_args(args):
    return _statements([BINBASH] + 
                       [SBATCH_COMMENT + _assignment(_arg(name), value) 
                       for name, value in args.items()])
        

def export_path(path):
    return _statements([EXPORT + _assignment('PATH', _quote(path + ':' + _ref('PATH')))])

def touch_file(file_):
    return _statements([TOUCH + file_])

def make_directory(directory):
    return _statements([MKDIR +  _arg('p', shorthand=True) + ' ' + directory])
    
def pipe_command(in_, out_):
    return in_ + ' | ' + out_
    
def remove_file(file_):
    return _statements([REMOVE + _arg('rf') + ' ' + file_])

# Flow Control Elements
def _for_loop(list_, statement):
    return _statements(['for __entry__ in ' + list_,
                       'do',
                       _indent(statement),
                       'done'])

def _while_loop(cond, contents):
    return _statements(['while ' + cond + '; do', 
                        _indent(contents), 
                        'done'])

def _if_statement(cond, contents):
    return _statements(['if ' + cond + '; then', 
                        _indent(contents), 
                        'fi'])

def _case_statement(case, cases):
    inner = []
    for c, contents in cases.items():
         inner.append(_indent(_statements([c + ')',  _indent(contents), ';;'])))
    return _statements(['case ' + case + ' in', 
                        _statements(inner), 
                        'esac'])

def _statements(statements_):
    return NEW_LINE.join(statements_)

# Expression Elements
def _cond(exp): return '[ ' + exp + ' ]' 

def _and(exp1, exp2): return _cond(exp1) +  ' && ' + _cond(exp2)

def _or(exp1, exp2): return _cond(exp1) + ' || ' + _cond(exp2)

def _not_equal(exp1, exp2): return exp1 + ' != ' + exp2

def _equal(exp1, exp2): return exp1 + ' = ' + exp2

def _less_than(exp1, exp2): return exp1 + ' ' + _arg('lt', shorthand=True) + ' ' + exp2

def _assignment(var, exp): return var + '=' + str(exp)

def _increment(var): return 'let ' + _quote(var + '++')

def _sleep(seconds): return SLEEP + str(seconds)

def _ref(var): return '$' + var  

def _extention(statment, extention_): return statment + '.' + extention_

def _arg(name, shorthand=False): 
    if shorthand: return '-' + name 
    else: return '--' + name
        
def _quote(var): return '"' + str(var) + '"'

# Formatting
def _indent(contents): return textwrap.indent(contents, TAB)