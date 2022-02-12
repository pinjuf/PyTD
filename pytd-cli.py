#!/usr/bin/env python3

from pytd import Task, TaskList
import os

tasklist = TaskList()

# TODO: If filename is empty, check if DEFAULT_FILENAME exists
tasklist.filename = input("Filename of TaskList    : ")
if os.path.exists(tasklist.filename):
    tasklist.load()
else:
    tasklist.title = input("Name of TaskList        : ")
    tasklist.desc = input("Description of TaskList : ")

current = tasklist

while True:
    cmd = input("PyTD> ").strip()

    if not cmd:
        continue
    try:
        if cmd in ("l", "ls", "list", "show"):
            print(current.pretty_show())
        elif cmd.split()[0] in ("s", "select"):
            index = int(cmd.split()[1]) -1
            current = current.subtasks[index]
        elif cmd in ("u", "up"):
            if current.parent:
                current = current.parent
        elif cmd in ("w", "write", "save"):
            tasklist.save()
        elif cmd in ("q", "quit", "exit"):
            exit(0)
        elif cmd in ("x", "wq"):
            tasklist.save()
            exit(0)
        elif cmd.split()[0] in ("d", "done"):
            if len(cmd.split())>1:
                current.subtasks[int(cmd.split()[1])-1].set_done(True)
            else:
                current.set_done(True)
        elif cmd.split()[0] in ("U", "undo", "undone"):
            if len(cmd.split())>1:
                current.subtasks[int(cmd.split()[1])-1].set_done(False)
            else:
                current.set_done(False)
        elif cmd.split()[0] in ("r", "remove", "del", "delete"):
            del current.subtasks[int(cmd.split()[1])-1]
        elif cmd in ("root"):
            current = tasklist
        else:
            raise Exception()
    except:
        print("Something didn't work out with your command.")

tasklist.save()