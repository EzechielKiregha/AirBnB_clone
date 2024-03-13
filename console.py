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
from models.engine.errors import *


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
                        printedObj += str(obj)
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

    def default(self, arg):
        """Override default method to handle class methods"""
        if '.' in arg and arg[-1] == ')':
            if arg.split('.')[0] not in storage.models:
                print("** class doesn't exist **")
                return
            return self.handle_class_methods(arg)
        return cmd.Cmd.default(self, arg)

    def do_models(self, arg):
        """Print all registered Models"""
        print(*storage.models)

    def handle_class_methods(self, arg):
        """Handle Class Methods
        <cls>.all(), <cls>.show() etc
        """

        printable = ("all(", "show(", "count(", "create(")
        try:
            val = eval(arg)
            for x in printable:
                if x in arg:
                    print(val)
                    break
            return
        except AttributeError:
            print("** invalid method **")
        except InstanceNotFoundError:
            print("** no instance found **")
        except TypeError as te:
            field = te.args[0].split()[-1].replace("_", " ")
            field = field.strip("'")
            print(f"** {field} missing **")
        except Exception as e:
            print("** invalid syntax **")
            pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
