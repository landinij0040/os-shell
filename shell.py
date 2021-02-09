import os
# Use only
 # pipe()
 # fork()
 # dup() or dup2()
 # execve()
 # wait()
 # open() or create() and close()
 # read() and write()
 # chdir()
import sys
import re

'''
a)	Read a unix command from the user, execute it, and repeat. 
    Handle at least the basic commands (ls, cat, grep, etc., 
    typically found in /usr/bin), 
    with all their normal parameters. [5 points]
''' 
def a_normal_parameters(input):
    split_input = input.decode().split()
    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, split_input[0])
        try:
            os.execve(program, split_input, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly
        
    os.write(2, ("Could not exec %s\n" % input[0]).encode())
    sys.exit(1)
    
'''
f)	Also run commands that name a program anywhere in the path. 
[3 points]
'''    
def f_path_parameters(input):
    split_input = input.decode().split()
    try:
        os.execve(split_input[0], [split_input[0].split('/')[-1], split_input[1:]], os.environ) # try to exec program
    except FileNotFoundError:             # ...expected
        os.write(2, ("Could not exec %s\n" % input[0]).encode())
        sys.exit(1)
    

def is_valid_path(string):
    if string.decode()[0] == '/':
        return True
    else:
        return False

def wait_fork(input):
    rc = os.fork()
    if(is_valid_path(input)):
        if rc == 0:
            f_path_parameters(input)
        else:
            the_wait_value = os.waitpid(rc,0)
    else:      
        if rc == 0:
            a_normal_parameters(input)
        else:
            the_wait_value = os.waitpid(rc,0)

'''
d)	Support background tasks,  
    that is, tasks which run without requiring 
    the user to wait before the next command, 
    specified with &. [3 pts] 
'''     
def no_wait_fork(input):
    rc = os.fork()
    if(is_valid_path(input)):
        if rc == 0:
            f_path_parameters(input)
    else:      
        if rc == 0:
            a_normal_parameters(input)
    

if __name__ == "__main__":
    '''
    c)	Before reading each line, 
    print the prompt string specified by shell variable PS1,
    but if  PS1 is not set,
    use the default prompt of  $$$$.  [1 pt] 
    '''
    try:
        os.environ['PS1']
    except Exception:
        os.environ['PS1'] = "$$$$"
    
    
    while(1):
        command_prompt = os.getcwd() + os.environ['PS1']  
     
        os.write(1,command_prompt.encode())
        input = os.read(0, 10000)
        
        # b)	Terminate if the input is exit. [1 point] 
        if(input == b'exit\n'):
            exit();
        # picking which comman to use
        if len(input) > 0:
            the_amperand_check_list = input.decode().split()
            if the_amperand_check_list[-1] == '&':
                no_wait_fork(' '.join([str(elem) for elem in the_amperand_check_list[:-1]]).encode())
            else:    
                wait_fork(input)
       
        
    
