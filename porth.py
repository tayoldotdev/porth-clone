#!/usr/bin/env python3

import sys;
import subprocess;
from os import path;

iota_counter=0;

def iota(reset=False):
    global iota_counter;
    if (reset):
        iota_counter = 0;
    result = iota_counter;
    iota_counter += 1;
    return result;

OP_PUSH=iota();
OP_PLUS=iota();
OP_MINUS=iota();
OP_EQUAL=iota();
OP_DUMP=iota();
OP_IF=iota();
OP_ELSE=iota();
OP_END=iota();
OP_DUP=iota();
OP_GT=iota();
OP_WHILE=iota();
OP_DO=iota();
#OP_MEM=iota();
COUNT_OPS=iota();

def push(x):
    return (OP_PUSH, x);

def plus():
    return (OP_PLUS,);

def minus():
    return (OP_MINUS,);

def equal():
    return (OP_EQUAL,);

def dump():
    return (OP_DUMP,);

def iff():
    return (OP_IF,);

def elsee():
    return (OP_ELSE,);

def end():
    return (OP_END,);

def dup():
    return (OP_DUP,);

def gt():
    return (OP_GT,);

def whilee():
    return (OP_WHILE,);

def do():
    return (OP_DO,);


# Does not compile it just simulates the program
def out_simulate_program(program):
    stack = [];
    ip = 0;
    while ip < len(program):
        assert COUNT_OPS == 12, "Exhaustive handling of operations in simulation"
        op = program[ip];
        if op['type'] == OP_PUSH:
            stack.append(op['value']);
            ip += 1;
        elif op['type'] == OP_PLUS:
            a = stack.pop();
            b = stack.pop();
            stack.append(a + b);
            ip += 1;
        elif op['type'] == OP_MINUS:
            a = stack.pop();
            b = stack.pop();
            stack.append(b - a);
            ip += 1;
        elif op['type'] == OP_EQUAL:
            a = stack.pop();
            b = stack.pop();
            stack.append(int(a == b));
            ip += 1;
        elif op['type'] == OP_IF:
            a = stack.pop();
            if a == 0:
                assert 'jmp' in op, "`if` instruction does not have a reference to the end of it's block. Please call crossreference_blocks() on the program before you simulate it!";
                ip = op['jmp'];
            else:
                ip += 1;
        elif op['type'] == OP_ELSE:
            assert 'jmp' in op, "`else` instruction does not have a reference to the end of it's block. Please call crossreference_blocks() on the program before you simulate it!";
            ip = op['jmp'];
        elif op['type'] == OP_END:
            assert 'jmp' in op, "`end` instruction does not have a reference to the next instruction to jump to. Please call crossreference_blocks() on the program before you simulate it!";
            ip = op['jmp'];
        elif op['type'] == OP_DUP:
            a = stack.pop();
            stack.append(a);
            stack.append(a);
            ip += 1;
        elif op['type'] == OP_GT:
            b = stack.pop();
            a = stack.pop();
            stack.append(int(a > b));
            ip += 1;
        elif op['type'] == OP_WHILE:
            ip += 1;
        elif op['type'] == OP_DO:
            a = stack.pop();
            if a == 0:
                assert 'jmp' in op, "`do` instruction does not have a reference to the next instruction to jump to. Please call crossreference_blocks() on the program before you simulate it!";
                ip = op['jmp'];
            else:
                ip += 1;
        elif op['type'] == OP_DUMP:
            a = stack.pop();
            print(a);
            ip += 1;
        else:
            assert False, "unreachable";

# Does not simulte it just compiles
def compile_program(program, out_file_path):
    with open(out_file_path, "w") as out:
        out.write("dump:\n");
        out.write("    mov     r8, -3689348814741910323\n");
        out.write("    sub     rsp, 40\n");
        out.write("    mov     BYTE [rsp+31], 10\n");
        out.write("    lea     rcx, [rsp+30]\n");
        out.write(".L2:\n");
        out.write("    mov     rax, rdi\n");
        out.write("    mul     r8\n");
        out.write("    mov     rax, rdi\n");
        out.write("    shr     rdx, 3\n");
        out.write("    lea     rsi, [rdx+rdx*4]\n");
        out.write("    add     rsi, rsi\n");
        out.write("    sub     rax, rsi\n");
        out.write("    mov     rsi, rcx\n");
        out.write("    sub     rcx, 1\n");
        out.write("    add     eax, 48\n");
        out.write("    mov     BYTE [rcx+1], al\n");
        out.write("    mov     rax, rdi\n");
        out.write("    mov     rdi, rdx\n");
        out.write("    cmp     rax, 9\n");
        out.write("    ja      .L2\n");
        out.write("    lea     rdx, [rsp+32]\n");
        out.write("    mov     edi, 1\n");
        out.write("    sub     rdx, rsi\n");
        out.write("    mov     rax, 1\n");
        out.write("    syscall\n");
        out.write("    add     rsp, 40\n");
        out.write("    ret\n");
        out.write("%define SYS_EXIT 60\n");
        out.write("segment .text\n");
        out.write("global _start\n");
        out.write("_start:\n");
        for ip in range(len(program)):
            assert COUNT_OPS == 12, "Exhaustive handling of operations in compilation"
            op = program[ip];
            out.write("addr_%d:\n" % ip);
            if op['type'] == OP_PUSH:
                out.write(";;  -- push %d --\n" % op['value']);
                out.write("    push %d\n" % op['value']);
            elif op['type'] == OP_PLUS:
                out.write(";;  -- plus --\n");
                out.write("    pop rax\n");
                out.write("    pop rbx\n");
                out.write("    add rax, rbx\n");
                out.write("    push rax\n");
            elif op['type'] == OP_MINUS:
                out.write(";;  -- minus --\n");
                out.write("    pop rax\n");
                out.write("    pop rbx\n");
                out.write("    sub rbx, rax\n");
                out.write("    push rbx\n");
            elif op['type'] == OP_EQUAL:
                out.write(";;  --  equal --\n");
                out.write("    mov rcx, 0\n");
                out.write("    mov rdx, 1\n");
                out.write("    pop rax\n");
                out.write("    pop rbx\n");
                out.write("    cmp rax, rbx\n");
                # move 1 to rcx when rax == rbx
                out.write("    cmove rcx, rdx\n");
                out.write("    push rcx\n");
            elif op['type'] == OP_IF:
                out.write(";;  -- if --\n");
                out.write("    pop rax\n");
                out.write("    test rax, rax\n");
                assert 'jmp' in op, "`if` instruction does not have a reference to the end of it's block. Please call crossreference_blocks() on the program before you compile it!"
                out.write("    jz addr_%d\n" % op['jmp']);
            elif op['type'] == OP_ELSE:
                out.write(";;  -- else --\n");
                assert 'jmp' in op, "`else` instruction does not have a reference to the end of it's block. Please call crossreference_blocks() on the program before you compile it!"
                out.write("   jmp addr_%d\n" % op['jmp']);
            elif op['type'] == OP_END:
                assert 'jmp' in op, "`end` instruction does not have a reference to the next instruction to jump to. Please call crossreference_blocks() on the program before you compile it!";
                out.write(";;  -- end --\n");
                if ip + 1 != op['jmp']:
                    out.write("   jmp addr_%d\n" % op['jmp']);
            elif op['type'] == OP_DUP:
                out.write(";;  -- dup --\n");
                out.write("    pop rax\n");
                out.write("    push rax\n");
                out.write("    push rax\n");
            elif op['type'] == OP_GT:
                out.write(";;  -- gt --\n");
                out.write("    mov rcx, 0\n");
                out.write("    mov rdx, 1\n");
                out.write("    pop rbx\n");
                out.write("    pop rax\n");
                out.write("    cmp rax, rbx\n");
                # move 1 to rcx when rax == rbx
                out.write("    cmovg rcx, rdx\n");
                out.write("    push rcx\n");
            elif op['type'] == OP_WHILE:
                out.write(";;  -- while --\n");
            elif op['type'] == OP_DO:
                out.write(";;  -- do --\n");
                out.write("    pop rax\n");
                out.write("    test rax, rax\n");
                assert 'jmp' in op, "`do` instruction does not have a reference to the end of it's block. Please call crossreference_blocks() on the program before you compile it!"
                out.write("    jz addr_%d\n" % op['jmp']);
            elif op['type'] == OP_DUMP:
                out.write(";;  -- dump %d --\n");
                out.write("    pop rdi\n");
                out.write("    call dump\n");
            else:
                assert False, "unreachable";

        out.write("addr_%d:\n" % len(program));
        out.write("    mov rax, SYS_EXIT\n");
        out.write("    mov rdi, 0\n");
        out.write("    syscall\n");

def parse_token_as_op(token):
    (file_path, row, col, word) = token;
    loc = (file_path, row + 1, col + 1);
    assert COUNT_OPS == 12, "Exhaustive op handling in parse_token_as_op";
    if word == '+':
        return {'type': OP_PLUS, 'loc': loc};
    elif word == '-':
        return {'type': OP_MINUS, 'loc': loc};
    elif word == '=':
        return {'type': OP_EQUAL, 'loc': loc};
    elif word == 'if':
        return {'type': OP_IF, 'loc': loc};
    elif word == 'else':
        return {'type': OP_ELSE, 'loc': loc};
    elif word == 'end':
        return {'type': OP_END, 'loc': loc};
    elif word == 'dup':
        return {'type': OP_DUP, 'loc': loc};
    elif word == '>':
        return {'type': OP_GT, 'loc': loc};
    elif word == 'while':
        return {'type': OP_WHILE, 'loc': loc};
    elif word == 'do':
        return {'type': OP_DO, 'loc': loc};
    elif word == '.':
        return {'type': OP_DUMP, 'loc': loc};
    elif word == 'mem':
        return {'type': OP_MEM, 'loc': loc};
    else: 
        try:
            return {'type': OP_PUSH, 'value': int(word), 'loc': loc};
        except ValueError as err:
            print("%s:%d:%d: %s" % (file_path, row, col, err));
            exit(1);

def crossreference_blocks(program):
    stack = [];
    for ip in range(len(program)):
        assert COUNT_OPS == 12, "Exhaustive handling of ops in crossreference_blocks"
        op = program[ip]; 
        if op['type'] == OP_IF:
            stack.append(ip);
        elif op['type'] == OP_ELSE:
            if_ip = stack.pop();
            if program[if_ip]['type'] != OP_IF:
                print("%s:%d:%d:  Error `else` can only be used in `if`-blocks" % program[if_ip]['loc']);
                exit(1);
            program[if_ip]['jmp'] = ip + 1;
            stack.append(ip);
        elif op['type'] == OP_END:
            block_ip = stack.pop();
            if program[block_ip]['type'] == OP_IF or program[block_ip]['type'] == OP_ELSE:
                program[block_ip]['jmp'] = ip;
                program[ip]['jmp'] = ip + 1;
            elif program[block_ip]['type'] == OP_DO:
                assert len(program[block_ip]) >= 2;
                program[ip]['jmp'] = program[block_ip]['jmp'];
                program[block_ip]['jmp'] = ip + 1;
            else: 
                print("%s:%d:%d: ERROR: `end` can only close `if`, `else` or `do` blocks" % program[block_ip]['loc']);
                exit(1);
        elif op['type'] == OP_WHILE:
            stack.append(ip);
        elif op['type'] == OP_DO:
            while_ip = stack.pop();
            program[ip]['jmp'] = while_ip;
            stack.append(ip);

    if len(stack) > 0:
        print('%s:%d:%d: ERROR: unclosed block' % program[stack.pop()]['loc'])
        exit(1)

    return program;

def find_col(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start += 1;
    return start;

def lex_line(line):
    col = find_col(line, 0, lambda x: not x.isspace());
    while col < len(line):
        col_end = find_col(line, col, lambda x: x.isspace());
        yield (col, line[col:col_end]);
        col = find_col(line, col_end, lambda x: not x.isspace());

def lex_file(file_path):
    with open(file_path, 'r') as f:
        return [(file_path, row, col, token)
            for (row, line) in enumerate(f.readlines())
            for (col, token) in lex_line(line.split('//')[0])];

def load_program_from_file(file_path):
        return crossreference_blocks([parse_token_as_op(token) for token in lex_file(file_path)]);

def print_usage(program):
    print("Usage: %s <SUBCOMMAND> [ARGS]" % (program));
    print("SUBCOMMAND:");
    print("    sim <file>           ... Simulate the program");
    print("    com [OPTIONS] <file> ... Compile the ptogram");
    print("      OPTIONS:");
    print("        -r               ... Run the program after successful compilation");
    print("        -o <file|dir>    ... Customize the output path")
    print("    help                 ... Print this help to stdout and exit with 0 code")



def call_cmd(cmd):
    print("+", ' '.join(cmd));
    subprocess.call(cmd);

if __name__ == '__main__':
    argv = sys.argv;
    assert len(argv) >= 1;
    compiler_name, *argv = argv;
    if len(argv) < 1:
        print_usage(compiler_name);
        print("ERROR: no subcommand provided");
        exit(1);

    subcommand, *argv = argv;

    if subcommand == "sim":
        if len(argv) < 1:
            print_usage(compiler_name);
            print("ERROR: No input file was provided for the simulation");
            exit(1);
        program_path, *argv = argv;
        program = load_program_from_file(program_path);
        simulate_program(program); 
    elif subcommand == "com":
        should_execute = False;
        program_path = None;
        output_path  = None;
        while len(argv) > 0:
            flag, *argv = argv;
            if flag == '-r':
                should_execute = True;
            elif flag == '-o':
                if len(argv) == 0:
                    print_usage(compiler_name)
                    print("ERROR: no argument is provided for parameter -o")
                    exit(1)
                output_path, *argv = argv
            else:
                program_path = flag;
                break;

        if program_path is None:
            print_usage(compiler_name);
            print("ERROR: no input file provided for compilation");
            exit(1);

        out_basename = None
        out_basedir = None
        if output_path is not None:
            if path.isdir(output_path):
                out_basename = path.basename(program_path)
                porth_ext = '.porth'
                if out_basename.endswith(porth_ext):
                    out_basename = out_basename[:-len(porth_ext)]
                out_basedir = path.dirname(output_path)
            else:
                out_basename = path.basename(output_path)
                out_basedir = path.dirname(output_path)
        else:
            out_basename = path.basename(program_path)
            porth_ext = '.porth'
            if out_basename.endswith(porth_ext):
                out_basename = out_basename[:-len(porth_ext)]
            out_basedir = path.dirname(program_path)
        out_basepath = path.join(out_basedir, out_basename)

        print("[INFO] Generating %s" % (out_basepath + ".asm"))
        program = load_program_from_file(program_path);
        compile_program(program, out_basepath + ".asm")
        call_cmd(["nasm", "-felf64", out_basepath + ".asm"])
        call_cmd(["ld", "-o", out_basepath, out_basepath + ".o"])
        if should_execute:
            call_cmd([out_basepath])

    else:
        print_usage(compiler_name);
        print("ERROR: unknown subcommand '%s'" % (subcommand));
        exit(1);
