




class CommandStack:

    def __init__(self):
        i = 1
        self.cmd_lst = ["bottom"]
        self.cmd_ptr = 0


    def push(self, info):
        self.cmd_lst.append(info)
        self.cmd_ptr += 1
        return self.cmd_ptr


    def pop(self):
        info = None
        if self.cmd_ptr > 0: 
            info = self.cmd_lst.pop()
            self.cmd_ptr -= 1 
        return info


    def size(self):
        return len(self.cmd_lst)


    def peek(self, ptr):
        if ptr < 0 or self.cmd_ptr <= ptr:
            return None
        info = self.cmd_lst[ptr]
        return info


    def isEmpty(self):
        is_empty = True
        if len(self.cmd_lst) > 1:
            is_empty = False
        return is_empty



class CommandInfo:

    def __init__(self): 
        self.module = ""
        self.cmd    = ""
        self.params = None

# params are either [...] or None
