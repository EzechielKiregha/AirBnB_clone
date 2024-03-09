#!/usr/bin/python3
"""This module contains the console for the Airbnb clone project."""
import cmd
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the Airbnb clone project."""

    class_list = ["BaseModel", "User", "Place", "State\
", "City", "Amenity", "Review"]
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Exit the program when EOF is reached (Ctrl+D)."""
        return True

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_create(self, arg):
        """
        Create a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        """
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            cls_name = args[0]
            obj_id = args[1]
            obj_key = "{}.{}".format(cls_name, obj_id)
            print(storage.all()[obj_key])
        except IndexError:
            if cls_name not in HBNBCommand.class_list:
                print("** class doesn't exist **")
            else:
                print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            cls_name = args[0]
            obj_id = args[1]
            obj_key = "{}.{}".format(cls_name, obj_id)
            del storage.all()[obj_key]
            storage.save()
        except IndexError:
            if cls_name not in HBNBCommand.class_list:
                print("** class doesn't exist **")
            else:
                print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        args = arg.split()
        if len(args) == 0:
            print([str(obj) for obj in storage.all().values()])
        else:
            try:
                cls_name = args[0]
                if cls_name not in HBNBCommand.class_list:
                    print("** class doesn't exist **")
                    return
                printedObj = ""
                for obj in storage.all().values():
                    if type(obj).__name__ == cls_name:
                        printedObj.append(str(obj))
                print(printedObj)
            except IndexError:
                print("** class name missing **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        print(args[0], args[1])
        if len(args) == 0:
            print("** class name missing **")
            return
        cls_name = args[0]
        if cls_name not in HBNBCommand.class_list:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
            return
        else:
            obj_id = args[1]
            obj_key = "{}.{}".format(cls_name, obj_id)
            if obj_key not in storage.all().keys():
                print("** no instance found **")
                return
            obj = storage.all()[obj_key]
            attr_name = args[2]
            attr_value = args[3]
            if hasattr(obj, attr_name):
                attr_type = type(getattr(obj, attr_name))(attr_value)
                setattr(obj, attr_name, attr_type)
                obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
