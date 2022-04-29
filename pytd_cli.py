#!/usr/bin/env python3

from pytd import Task, TaskList, DEFAULT_FILENAME
import os, sys

with open("data/cli-help", "r") as file:
    CLI_HELP = file.read()

def ask(prompt, condition=lambda i: i != ""):
    output = ""
    while not condition(output:=input(prompt)):
        pass
    return output

tasklist = TaskList()

if len(sys.argv)==2:
    tasklist.filename = sys.argv[1]
else:
    tasklist.filename = input("[?] Filename of TaskList    : ")
if not tasklist.filename:
    tasklist.filename = DEFAULT_FILENAME
if os.path.exists(tasklist.filename):
    tasklist.load()
else:
    tasklist.title = ask("[?] Name of TaskList        : ")
    tasklist.desc = input("[?] Description of TaskList : ")

current = tasklist

while True:
    try:
        cmd = input("[P] PyTD> ").strip()
    except:
        exit(0)

    if not cmd:
        print("[i] Use \"help\" to view this programs usage.")
        continue
    try:
        if cmd in ("h", "help"):
            print(CLI_HELP)

        elif cmd in ("l", "ls", "list", "show"):
            print(current.pretty_path())
            print(current.pretty_show())

        elif cmd.split()[0] in ("s", "select"):
            index = int(cmd.split()[1]) -1
            current = current.subtasks[index]

        elif cmd in ("u", "up"):
            if current.parent:
                current = current.parent
            else:
                print("[!] You are at top of your TaskList")

        elif cmd in ("w", "write", "save"):
            tasklist.save()

        elif cmd in ("q", "quit", "exit"):
            exit(0)

        elif cmd in ("x", "wq"):
            tasklist.save()
            exit(0)

        elif cmd.split()[0] in ("d", "do", "done"):
            task = current.subtasks[int(cmd.split()[1])-1] if len(cmd.split())==2 else current
            if not task.can_be_done():
                print("[!] You have not done the required tasks to finish this task.")
            task.set_done(True)
        elif cmd.split()[0] in ("U", "undo", "undone"): # i have no idea why parents are automatically set as undone too, but it works
            if len(cmd.split())==2:
                current.subtasks[int(cmd.split()[1])-1].set_done(False)
            else:
                current.set_done(False)

        elif cmd.split()[0] in ("r", "remove", "del", "delete"):
            del current.subtasks[int(cmd.split()[1])-1]

        elif cmd in ("root",):
            current = tasklist

        elif cmd in ("n", "new", "add"):
            current.add_subtask(Task(title=ask("[?] Name of task: "),desc=input("[?] Description of the task: ")))

        elif cmd in ("t", "tree"):
            print(current.pretty_tree())

        elif cmd in ("rt", "roottree", "rtree"):
            print(tasklist.pretty_tree())

        else:
            raise Exception()
    except:
        print("[!] Something didn't work out with your command.")

tasklist.save()
