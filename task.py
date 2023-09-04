#!/usr/bin/env python3
from os import environ


def cli():
    @command
    def start():
        dev_compose("up", "--detach", "--build")

    @command
    def start_shell():
        dev_compose("run", "--build", "cow", "bash")

    @command
    def attach_shell():
        dev_compose("exec", "cow", "bash")

    @command
    def stop():
        dev_compose("down", "--volumes")

    @command
    def start_bash():
        dev_compose("exec", "cow", "bash")


def dev_compose(*args, **kwargs):
    compose(["build", "dev"], *args, env=dict(environ, COW_VERSION="dev"), **kwargs)


def compose(variants: list[str], *args, **kwargs):
    variant_args = flatten(
        [["--file", f"src/docker-environment/docker-compose.{v}.yml"] for v in variants]
    )

    cmd(
        "docker",
        "compose",
        "--project-directory",
        ".",
        "--file",
        "src/docker-environment/docker-compose.yml",
        *variant_args,
        *args,
        **kwargs,
    )


# https://realpython.com/python-flatten-list/#using-a-comprehension-to-flatten-a-list-of-lists
def flatten(matrix):
    return [item for row in matrix for item in row]


# fmt: off
# https://gist.github.com/sirikon/d4327b6cc3de5cc244dbe5529d8f53ae
import inspect, sys, os, subprocess, re;commands = [];args = sys.argv[1:]
def _c(c): return f'\x1b[{c}m' # Change to `return ''` to disable colors
def cmd(*args, check=True, **k): return subprocess.run(args, check=check, **k)
def command(func): commands.append(func); return func
def _default(i, spec): d=spec.defaults;m=len(spec.args)-len(d or []);return\
    (True,f'={d[i-m]}'if d[i-m]is not None else'') if i >= m else (False,'')
def _ri(s, n): s=re.sub('^[ ]*\n', '', s);s=re.sub('\n[ ]*$', '', s);\
    ls=s.split('\n');i=len(re.match('(^[ ]*)', ls[0]).group(0));\
    return '\n'.join((n * ' ') + re.sub(f'^[ ]{{{i}}}', '', l) for l in ls)
os.chdir(os.path.dirname(__file__));cli()
if len(args) == 0: print(f"{_c(1)}commands:{_c(0)}"); [print(' '.join([
    f'  {_c(96)}{f.__name__}{_c(0)}',
    *[f'{_c(36)}({a}{d[1]}){_c(0)}' if d[0] else f'{_c(36)}[{a}]{_c(0)}' \
        for a,d in ((a,_default(i, spec)) for i, a in enumerate(spec.args))],
    *([f'[...{spec.varargs}]'] if spec.varargs is not None else []),
    *([f'\n{_c(2)}{_ri(f.__doc__, 4)}{_c(0)}'] if f.__doc__ else [])
]))for spec, f in((inspect.getfullargspec(f), f) for f in commands)];exit(0)
matching_commands = [f for f in commands if f.__name__ == args[0]]
if len(matching_commands)==0:print(f'Unknown command "{args[0]}"');sys.exit(1)
try: matching_commands[0](*args[1:])
except KeyboardInterrupt: pass
except subprocess.CalledProcessError as err: sys.exit(err.returncode)