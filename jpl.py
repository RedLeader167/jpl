import json
import sys
import operator


operators = {
  "==": operator.eq,
  "!=": operator.ne,
  ">": operator.gt,
  ">=": operator.ge,
  "<": operator.lt,
  "<=": operator.le
}

code = """
[
    ["var", "message", "Hello World!"],
    ["var", "cois", "Counter value is"],
    ["var", "counter", 0],
    ["print","^&message\\nIf:"],
    [
        "if", [6, "==", 6], 
        [
            ["math", "add", "^&counter", 1], 
            ["print", "^&cois ^&counter"]
        ]
    ],
    ["print", "While:"],
    [
        "while", ["^&counter", "!=", 11],
        [
            ["print", "^&cois ^&counter"],
            ["math", "add", "^&counter", 1]
        ]
    ],
    [
        "try",
        [
            ["print"]
        ],
        [
            ["print", "error"]
        ]
    ],
    ["print", "ok"],
    ["fn", "sayGay",
        [
            ["print", "you gay"]
        ]
    ],
    ["fncall", "sayGay"]
]
"""

fc = json.loads(code)

#print(fc)
varTable = {}
fnTable = {}
codePtr = 0

def argck(args, index, ise=False):
    if True:
        global codePtr
        line = codePtr
    if len(args) > index:
        return True
    if not ise:
        print(f"Error at line {str(line)}: not enough arguments")
    return False

def isArg(arg, argin, ise=False):
    global codePtr
    if isinstance(arg, argin):
        return True
    if not ise:
        print(f"Error at line {str(codePtr)}: wrong argument type")
    return False

def procArg(arg):
    global varTable
    rt = str(arg)
    for key in list(varTable.keys()):
        rt = rt.replace(key, str(varTable[key]))
    rd = {
        "\\bs": "\\",
        "\\pow": "^",
        "\\n": "\n",
        "\\t": "\t"
    }
    for key in list(rd.keys()):
        rt = rt.replace(key, rd[key])
    return rt

def ifp(ca, ise=False):
    if operators[ca[1][1]](procArg(ca[1][0]), procArg(ca[1][2])):
        isArg(ca[2], list, ise)
        tmpc = 0
        while tmpc < len(ca[2]):
            if not process(ca[2][tmpc], ise): return False
            tmpc += 1

def whilep(ca, ise=False):
    argck(ca, 2, ise)
    isArg(ca[2], list, ise)
    global codePtr
    while operators[ca[1][1]](procArg(ca[1][0]), procArg(ca[1][2])):
        tmpc = 0
        while tmpc < len(ca[2]):
            if not process(ca[2][tmpc], ise): return False
            tmpc += 1

def process(ca, ise=False):
    global codePtr
    global varTable
    ignoreErrors = ise
    if isinstance(ca, list):
        #print(ca) 
        if not argck(ca, 0, ise): return False
        if ca[0] == "print":
            if not argck(ca, 1, ise): return False
            print(procArg(ca[1]))
        elif ca[0] == "var":
            if not argck(ca, 2, ise): return False
            varTable["^&" + str(ca[1])] = ca[2]
        elif ca[0] == "math":
            if not argck(ca, 1, ise): return False
            if ca[1] == "add":
                if not argck(ca, 3, ise): return False
                varTable[ca[2]] += ca[3]
        elif ca[0] == "if":
            if not argck(ca, 1, ise): return False
            if not isArg(ca[1], list, ise): return False
            if not argck(ca[1], 2, ise): return False
            ifp(ca, ise)
        elif ca[0] == "while":
            if not argck(ca, 1, ise): return False
            if not isArg(ca[1], list, ise): return False
            if not argck(ca[1], 2, ise): return False
            whilep(ca, ise)
        elif ca[0] == "fn":
            if not argck(ca, 2, ise): return False
            if not isArg(ca[2], list, ise): return False
            fnTable[ca[1]] = ca[2]
        elif ca[0] == "fncall":
            if not argck(ca, 1, ise): return False
            tmpc = 0
            while tmpc < len(fnTable[ca[1]]):
                if not process(fnTable[ca[1]][tmpc], ise): return False
                tmpc += 1
        elif ca[0] == "try":
            if not argck(ca, 1, ise): return False
            if not isArg(ca[1], list, ise): return False
            tmpc = 0
            fail = False
            while tmpc < len(ca[1]):
                if not process(ca[1][tmpc], True):
                    fail = True
                    break
                tmpc += 1
            if True:
                if not argck(ca, 2, ise): return False
                if not isArg(ca[2], list, ise): return False
                if fail:
                    tmpc = 0
                    while tmpc < len(ca[2]):
                        if not process(ca[2][tmpc],ise): return False
                        tmpc += 1
        else:
            if not ignoreErrors:
                print(f"Error at line {str(codePtr)}: unknown command")
            return False
        return True
    else:
        if not ignoreErrors:
            print(f"Error at line {str(codePtr)}: should be list")
        return False

if isinstance(fc, list):
    while codePtr < len(fc):
        ca = fc[codePtr]
        res = process(ca)
        if not res: break
        codePtr += 1
else:
    print("Invalid code, should be array/list")