#!/usr/bin/env python3
import re
import sys
import os


def _ensure_mem(mem, mem_type, idx):
    if idx >= len(mem):
        ext = idx - len(mem) + 1
        mem.extend([None] * ext)
        mem_type.extend([''] * ext)

def _resolve_cell_numeric(mem, mem_type, idx):
    _ensure_mem(mem, mem_type, idx)
    t = mem_type[idx]
    v = mem[idx]
    if t == 'num':
        return v if isinstance(v, int) else 0
    if t == 'char' and isinstance(v, str) and v:
        return ord(v[0])
    return 0

def _sanitize_math_expr(expr):
    if not re.fullmatch(r"[0-9\[\]\s+\-*/%().]*", expr):
        raise ValueError("Math expression contains invalid characters")
    return expr

def compile_slashlang(src: str, indent=1):
    code = []
    tab = "    " * indent
    i = 0
    L = len(src)
    while i < L:
        c = src[i]
        
        if c == "_":
            code.append(f"{tab}cap = True")
            i += 1
            continue


        if c == "/":
            n = 1
            while i+n < L and src[i+n] == "/":
                n += 1
            code.append(f"{tab}mem[p] = chr((65 if cap else 97) + {n}-1)")
            code.append(f"{tab}mem_type[p] = 'char'")
            code.append(f"{tab}cap = False")
            i += n
            continue

        
        if c == ".":
            code.append(f"{tab}_ensure_mem(mem, mem_type, p)")
            code.append(f"{tab}if mem[p] is None:")
            code.append(f"{tab}    mem[p] = 'a'")
            code.append(f"{tab}    mem_type[p] = 'char'")
            code.append(f"{tab}elif mem_type[p] == 'num':")
            code.append(f"{tab}    try:")
            code.append(f"{tab}        mem[p] = chr(ord('a') + int(mem[p]) - 1)")
            code.append(f"{tab}        mem_type[p] = 'char'")
            code.append(f"{tab}    except:")
            code.append(f"{tab}        mem[p] = 'a'")
            code.append(f"{tab}        mem_type[p] = 'char'")
            i += 1
            continue

        
        if c == "n":
            n = 1
            while i+n < L and src[i+n] == "n":
                n += 1
            code.append(f"{tab}mem[p] = (-{n} if cap else {n})")
            code.append(f"{tab}mem_type[p] = 'num'")
            code.append(f"{tab}cap = False")
            i += n
            continue

        
        if c == ";":
            code.append(f"{tab}inp = input(''+str(p)+' > ')")
            code.append(f"{tab}try: mem[p] = int(inp)")
            code.append(f"{tab}except: mem[p] = 0")
            code.append(f"{tab}mem_type[p]='num'")
            i += 1
            continue

        
        if c == "\\":
            count = 1
            while i+count < L and src[i+count] == "\\":
                count += 1
            code.append(f"{tab}__bs_count = {count}")
            code.append(f"{tab}while __bs_count>0:")
            code.append(f"{tab}    if __bs_count>=3: out.append('\\n'); __bs_count-=3; continue")
            code.append(f"{tab}    if __bs_count==2: out.append(' '); __bs_count-=2; continue")
            code.append(f"{tab}    if __bs_count==1:")
            code.append(f"{tab}        if mem_type[p]=='char': out.append(mem[p])")
            code.append(f"{tab}        elif mem_type[p]=='num': out.append(str(mem[p]))")
            code.append(f"{tab}        __bs_count-=1")
            i += count
            continue

        
        if c == "[":
            code.append(f"{tab}p += 1")
            code.append(f"{tab}if p>=len(mem): mem.extend([None]*100); mem_type.extend(['']*100)")
            i += 1
            continue
        if c == "]":
            code.append(f"{tab}p -= 1")
            code.append(f"{tab}if p<0: p=0")
            i += 1
            continue

        
        if c == "m" and i+1 < L and src[i+1] == "/":
            j = i+2; expr=[]
            while j < L:
                if src[j] == "m" and j+1 < L and src[j+1] == "\\":
                    break
                expr.append(src[j]); j += 1
            if j >= L: raise SyntaxError("Unterminated math block")
            expr_text = "".join(expr).strip()

            code.append(f"{tab}if mem_type[p]=='char': mem[p]=_resolve_cell_numeric(mem,mem_type,p); mem_type[p]='num'")
            code.append(f"{tab}expr_raw={repr(expr_text)}")
            code.append(f"{tab}expr_clean=_sanitize_math_expr(expr_raw)")
            code.append(f"{tab}def _replace_idx(m):")
            code.append(f"{tab}    idx=int(m.group(1)); return str(_resolve_cell_numeric(mem,mem_type,idx))")
            code.append(f"{tab}expr_sub=re.sub(r'\\[(\\d+)\\]', _replace_idx, expr_clean)")
            code.append(f"{tab}mem[p]=eval(expr_sub, {{'__builtins__':None}}, {{}})")
            code.append(f"{tab}mem_type[p]='num'")
            i = j+2
            continue


        if c == "<":
            j = i+1 
            if j < L and src[j] == "[":
                j += 1
                idx = []
                while j < L and src[j] != "]":
                    idx.append(src[j])
                    j += 1
                if j >= L:
                    raise SyntaxError("Unterminated [idx] in loop count")
                j += 1

                index_num = int("".join(idx))
                code.append(f"{tab}__loop_count = _resolve_cell_numeric(mem, mem_type, {index_num})")
            else:
                num = []
                while j < L and src[j].isdigit():
                    num.append(src[j])
                    j += 1
                if not num:
                    raise SyntaxError("Missing loop count in <...>")
                count = int("".join(num))
                code.append(f"{tab}__loop_count = {count}")
            body = []
            while j < L:
                if src[j] == ">":
                    break
                body.append(src[j])
                j += 1

            if j >= L:
                raise SyntaxError("Unterminated loop <...>")

            inner_src = "".join(body).strip()

            code.append(f"{tab}for _ in range(__loop_count):")
            if inner_src:
                inner = compile_slashlang(inner_src, indent+1)
                code.extend(inner)
            else:
                code.append(f"{tab}    pass")
            i = j + 1
            continue

        if c == "p" and i+1 < L and src[i+1] == "/":
            j = i+2; snip=[]
            while j < L:
                if src[j]=="p" and j+1<L and src[j+1]=="\\": break
                snip.append(src[j]); j+=1
            if j>=L: raise SyntaxError("Unterminated python block")

            snippet="".join(snip)
            code.append(f"{tab}_ctx={{'mem':mem,'mem_type':mem_type,'p':p,'out':out,'__builtins__':{{}}}}")
            code.append(f"{tab}exec({repr(snippet)}, {{}}, _ctx)")
            code.append(f"{tab}p=_ctx['p']; mem=_ctx['mem']; mem_type=_ctx['mem_type']; out=_ctx['out']")
            i = j+2
            continue
        
        
        if c in "op":
            j = i+1
            if j < L and src[j] == "[":
                j+=1
                idx=[]
                while j<L and src[j]!="]": idx.append(src[j]); j+=1
                if j>=L: raise SyntaxError("Unterminated index")
                code.append(f"{tab}target_val=_resolve_cell_numeric(mem,mem_type,{int(''.join(idx))})")
            else:
                lit=[]
                while j < L and src[j].isdigit(): lit.append(src[j]); j+=1
                if not lit: raise SyntaxError("Missing literal in comparison")
                code.append(f"{tab}target_val={int(''.join(lit))}")

            code.append(f"{tab}cur_val=_resolve_cell_numeric(mem,mem_type,p)")
            op = "<" if c=="o" else ">"
            code.append(f"{tab}mem[p]=1 if (cur_val {op} target_val) else 0")
            code.append(f"{tab}mem_type[p]='num'")
            i = j
            continue


        if c == "$":
            while i < L and src[i] != "\n":
                i += 1
            continue


        
        if c == "+":
            code.append(f"{tab}_ensure_mem(mem,mem_type,p)")
            code.append(f"{tab}if mem[p] is None: mem[p]=1; mem_type[p]='num'")
            code.append(f"{tab}elif mem_type[p]=='num': mem[p]+=1")
            code.append(f"{tab}elif mem_type[p]=='char': mem[p]=chr(ord(mem[p])+1)")
            i+=1
            continue

        
        if c == "-":
            code.append(f"{tab}_ensure_mem(mem,mem_type,p)")
            code.append(f"{tab}if mem[p] is None: mem[p]=-1; mem_type[p]='num'")
            code.append(f"{tab}elif mem_type[p]=='num': mem[p]-=1")
            code.append(f"{tab}elif mem_type[p]=='char': mem[p]=chr(ord(mem[p])-1)")
            i+=1
            continue

        i += 1

    return code

def run_slash(src: str):
    header = [
        "def main():",
        "    import re",
        "    mem=[None]*200",
        "    mem_type=['']*200",
        "    p=0",
        "    out=[]",
        "    cap=False"
    ]
    body = compile_slashlang(src)
    footer = [
        "    print(''.join(out))",
        "    return ''.join(out)",
        "",
        "main()"
    ]
    full = "\n".join(header + body + footer)

    globs = {
        "_ensure_mem": _ensure_mem,
        "_resolve_cell_numeric": _resolve_cell_numeric,
        "_sanitize_math_expr": _sanitize_math_expr,
        "re": re
    }
    exec(full, globs, {})



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: day <file.day>")
        sys.exit(1)

    fname = sys.argv[1]

    if not os.path.exists(fname):
        print(f"Error: '{fname}' not found")
        sys.exit(1)

    with open(fname) as f:
        src = f.read()

    run_slash(src)
