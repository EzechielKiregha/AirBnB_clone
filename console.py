#!usr/bin/python3

import cmd

class Command(cmd.Cmd):
    
    def __init__(self):
        super().__init__()
        self.users = {}
    
    def do_create(self, line):
        """
        The create function create a user and save him in dictionary 
        syntax: create <id:int> <name:str>
        
        """
        args = line.split()
        if len(args) == 2:
            id, name = args
            if isinstance(id, str):
                id = int(id)
            self.users[id] = name
            print(f"User Recorded Successfully!")
            
        else:
            print("correct syntax: create <digit> <name>")
            
    def do_read(self, line):
        """The 'read' function read all available users in the dictionary"""
        print("All Users: ")
        for id, name in self.users.items():
            print(f"ID: {id} and Name: {name}")
        
    def do_EOF(self, line):
        """Interupt the execution and return True"""
        print()
        return True
    
    def do_quit(self, line):
        """Exit the console interpreter with succes exit status (0)"""
        exit(0)
        
    def default(self, line: str) -> None:
        print("Unkown Command.")
        
        
if __name__ == "__main__":
    Command().cmdloop()