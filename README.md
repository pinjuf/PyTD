# PyTD
A TODO-list tool written in Python.
Its goal is to
 - provide a stable posibility to get a good view over all your TODOs
 - motivate you to actually finish your tasks instead of procrastinating

## Usage
You can either make your own implementation by just using `pytd.py` as a module,
or use `pytd-cli.py` for a rudimentary interface.

## Quick documentation
PyTD stores its tasklists as a YAML file, following this structure (for single tasks as well as tasklists):

```
<title>:
  desc: <oneline-description>
  done: <bool>
  subtasks:
    <requirements/smaller bits of the parent task, following the same structure>
```

> Tasks vs. TaskLists
> 
> A Task represent something that you have to do. It may have subtasks, a.k.a. smaller parts of a task. They are, from a structural standpoint, equal to a normal Task. A TaskList is also very similar to a Task, except that it has no parents (like you), and is therefore the root of your task structure. It's also what's actually saved.

## Coming soon
 - [ ] ncurses UI: have a smoother and more satisfying experience doing your tasks
