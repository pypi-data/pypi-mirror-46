import os
import sys

def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
    
def simple_read(file_name):
    '''simple_read data from specified file_name'''
    with open(file_name, "r", encoding="utf-8") as file:
        file_content = file.read().splitlines()
    return file_content
    
    
def justify(content, grid=True, frame=False, newline='\n', delimiter=';', justsize=4):
    ''' 
    convert text to justified
    parameters:
        content - text with newlines and delimiters, to be converted
        grid - True/False value, grid inside; default is True
        frame - True/False value, frame around; default is False
        newline - newline symbol; default is '\\n'
        delimiter - delimiter symbol; default is ';'
        justsize - justify size; default is 4
    '''
    if not (type(content) is str) or not content:
        return ''
        
    content = content.split(newline)
    content = [item.strip().split(delimiter) for item in content if item.strip()]
    maxRow = len(max(content, key=len))
    content = [item + [""]*(maxRow-len(item)) for item in content]
    transposed = list(map(list, zip(*content)))
    
    #signs
    if grid:
        horSign = '|'
    else:
        horSign = ' '
    vertSign = ' '
    lineLen = [max([len(part) for part in item]) for item in transposed]
    
    # 1st column to the left
    # justifiedParts = [[(' '*1 + part).ljust(lineLen[key]+justsize, vertSign) if not key else part.center(lineLen[key]+justsize, vertSign) for key, part in enumerate(item)] for item in content]
    
    # justify all columns in the same way
    justifiedParts = [[part.center(lineLen[key]+justsize, vertSign) for key, part in enumerate(item)] for item in content]
    content = [horSign.join(item) for item in justifiedParts]
    
    line = '+'.join(["-"*len(item) for item in justifiedParts[0]])      # with '+' in the cross
    # line = "-"*len(content[0])                                          # without '+'
    if frame:
        # edgeLine = line.join(['+']*2)                                                       # with crosses
        edgeLine = '-'.join(["-"*len(item) for item in justifiedParts[0]]).join(['+']*2)    # without crosses
        line = line.join(['|']*2)
        content = [item.join(['|']*2) for item in content]
        
    line = line.join(['\n']*2)
    
    if grid:
        out = line.join(content)
    else:
        out = "\n".join(content)
        
    if frame:
        out = '\n'.join([edgeLine, out, edgeLine])
    return out
    
    
def example():
    data = 'this;is;very;line;there\nthis;is;not now;is;line;the end\nthis;is;;line\nthis;;here;line;thing;end\nthis;is;not now;is;line;the end\nthis;is;;line\nthis;;here;line;thing;end\nthsdis;is;not now;is;line;the end\nthis;is;;line\nthis;;here;line;thing;end\nthis;is;not now;is;line;the end\nthis;is;;line\nthis;;here;line;thing;end'
    someSize = 10
    clear = justify(data, grid=False, frame=False, justsize=someSize)
    withFrame = justify(data, grid=False, frame=True, justsize=someSize)
    withGrid = justify(data, grid=True, frame=False, justsize=someSize)
    full = justify(data, grid=True, frame=True, justsize=someSize)
    
    print("String data:\n\n{}\n\n".format(data))
    print("Justified clear:\n\n{}\n\n".format(clear))
    print("Justified with frame:\n\n{}\n\n".format(withFrame))
    print("Justified with grid:\n\n{}\n\n".format(withGrid))
    print("Justified full:\n\n{}\n\n".format(full))
    return True
    
    
if __name__ == "__main__":
    pass
    # path = script_path()
    # args = sys.argv[1:]
    # example()
    
''' 
todo:
    -add delimiter option, for now: ';' +
    -add newline sign, for now: '\n'    +
    -add grid as option                 +
    -think of justify to center or left
    -clean up?
'''