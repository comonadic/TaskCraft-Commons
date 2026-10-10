"""Evaluate an explicit safe subset of spreadsheet formulas for counterfactual tests."""
import ast,operator,re,math
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}
FUN={'SUM':lambda *x:sum(x),'AVERAGE':lambda *x:sum(x)/len(x),'MIN':min,'MAX':max,'ABS':abs,'ROUND':round}
def evaluate(formula,resolve):
    text=formula.strip().lstrip('=').replace('$','').upper()
    def expand(m):
        a,i,b,j=m.groups()
        if a!=b:raise ValueError('only vertical ranges supported')
        return ','.join(a+str(k) for k in range(int(i),int(j)+1))
    text=re.sub(r'([A-Z]+)(\d+):([A-Z]+)(\d+)',expand,text)
    def visit(node):
        if isinstance(node,ast.Constant) and isinstance(node.value,(int,float)):return node.value
        if isinstance(node,ast.Name) and re.fullmatch('[A-Z]+[0-9]+',node.id):return resolve(node.id)
        if isinstance(node,ast.BinOp) and type(node.op) in OPS:return OPS[type(node.op)](visit(node.left),visit(node.right))
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):return (-1 if isinstance(node.op,ast.USub) else 1)*visit(node.operand)
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in FUN and not node.keywords:return FUN[node.func.id](*[visit(x) for x in node.args])
        raise ValueError('unsupported formula syntax')
    value=visit(ast.parse(text,mode='eval').body)
    if not math.isfinite(value):raise ValueError('nonfinite formula')
    return value

def equivalence(got,expected,values):
    result=[]
    for target in expected:
        success=target in got
        for case in range(4):
            inputs={k:v*(1+(case+1)*(i+1)*.013)+case for i,(k,v) in enumerate(values.items()) if k not in expected}
            def compute(formulas):
                seen=set();cache=dict(inputs)
                def resolve(cell):
                    if cell in cache:return cache[cell]
                    if cell in seen:raise ValueError('cyclic formula')
                    seen.add(cell);v=evaluate(formulas[cell],resolve);seen.remove(cell);cache[cell]=v;return v
                return resolve(target)
            try:success=success and math.isclose(compute(got),compute(expected),abs_tol=1e-5,rel_tol=1e-5)
            except (ValueError,KeyError,ZeroDivisionError,TypeError,SyntaxError):success=False
        result.append(success)
    return sum(result)/len(result)
