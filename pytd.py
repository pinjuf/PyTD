#!/usr/bin/env python3

import yaml

DEFAULT_FILENAME = "TODO.yml"

class Task():
    def __init__(self, title="???", desc="", subtasks=[]):
        self.title    = title
        self.done     = False
        self.desc     = desc
        self.parent = None
        self.subtasks = []
        for subtask in subtasks:
            self.add_subtask(subtask)
        self.subtasks = subtasks.copy()

    def build_dict(self):
        output = {}
        output[self.title] = {}
        output[self.title]["done"] = self.done
        output[self.title]["desc"] = self.desc
        output[self.title]["subtasks"] = {}
        for subtask in self.subtasks:
            output[self.title]["subtasks"] |= subtask.build_dict()
        return output

    def parse_dict(self, in_dict, title=None):
        title = title if title else list(in_dict.keys())[0]
        self.title = title
        self.done = in_dict[title]["done"]
        self.desc = in_dict[title]["desc"]
        self.subtasks = []
        for subtask_title in in_dict[title]["subtasks"].keys():
            st = Task()
            st.parse_dict(in_dict[title]["subtasks"], title=subtask_title)
            self.add_subtask(st)

    def can_be_done(self):
        output = True
        for subtask in self.subtasks:
            output &= subtask.get_done()
        return output

    def set_done(self, status):
        self.done = status
        self.update_done()

    def get_done(self):
        self.update_done()
        return self.done

    def update_done(self):
        self.done &= self.can_be_done()

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)
        subtask.parent = self
        self.update_done()

    def pretty_show(self, detailed=True):
        output = "[X] " if self.get_done() else "[ ] "
        output += self.title
        if detailed:
            output += "\n\t" + self.desc
            for index, subtask in enumerate(self.subtasks):
                output += "\n\t" + str(index+1) + ") " + subtask.pretty_show(detailed=False)
        return output

    def pretty_path(self):
        output = ""
        if self.parent:
            output += self.parent.pretty_path() + " > "
        output += self.title
        return output

    def pretty_tree(self):
        output = self.pretty_show(detailed=False)
        for subtask in self.subtasks:
            st = subtask.pretty_tree()
            for line in st.split("\n"):
                output += "\n\t" + line
        return output

    def path(self):
        output = [self]
        if self.parent:
            output = self.parent.path() + output
        return output

class TaskList(Task):

    def __init__(self, title="???", desc="", subtasks=[], filename=DEFAULT_FILENAME):
        self.title    = title
        self.done     = False
        self.desc     = desc
        self.parent = None
        self.subtasks = []
        for subtask in subtasks:
            self.add_subtask(subtask)
        self.filename = DEFAULT_FILENAME

    def save(self):
        with open(self.filename, "w") as file:
            self.build_yaml(file)
    def load(self):
        with open(self.filename, "r") as file:
            self.parse_yaml(file)

    def parse_yaml(self, in_yaml, title=None):
        self.parse_dict(yaml.safe_load(in_yaml), title=None)
    def build_yaml(self, stream=None):
        return yaml.dump(self.build_dict(), stream, default_flow_style=False, allow_unicode=True)
