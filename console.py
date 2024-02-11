#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def compare_blacket(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """
        Provides default behavior for a command-line interface (CLI)
        tool when the input is invalid or unrecognized.

        Parameters:
            - self: Reference to the current instance of the class.
            - arg: The input string representing the argument
        """
        dictionary = {
            "all": self.perform_all,
            "show": self.perform_show,
            "destroy": self.perform_displaiy,
            "count": self.do_count,
            "update": self.update_perform
        }
        oxxo = re.search(r"\.", arg)
        if oxxo is not None:
            Argv = [arg[:oxxo.span()[0]], arg[oxxo.span()[1]:]]
            oxxo = re.search(r"\((.*?)\)", Argv[1])
            if oxxo is not None:
                command = [Argv[1][:oxxo.span()[0]], oxxo.group()[1:-1]]
                if command[0] in dictionary.keys():
                    call = "{} {}".format(Argv[0], command[1])
                    return dictionary[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def quit_perform(self, arg):
        """
        Implements the quit command to exit the program.

        Parameters:
            - self: A reference to the current instance of the class.
            - arg: Additional arguments provided with the quit command.

        Returns:
            - True: Indicates successful execution of command and request
        """
        return True

    def handle_eof(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def perform_show(self, arg):
        """
        Display the string representation of a class instance with a given ID.

        Parameters:
        - self: A reference to the current instance of the class.
        - arg: A string containing the command and its arguments.

        Usage:
        - show <class> <id> or <class>.show(<id>)
        """
        args = compare_blacket(arg)
        object_dictionary = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in object_dictionary:
            print("** no instance found **")
        else:
            print(object_dictionary["{}.{}".format(args[0], args[1])])

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        parsed_args = compare_blacket(arg)
        current = 0
        for obj in storage.all().values():
            if parsed_args[0] == obj.__class__.__name__:
                current += 1
        print(current)

    def perform_displaiy(self, arg):
        """
        Delete a class instance with a given ID.

        Parameters:
        - self: A reference to the current instance of the class.
        - arg: A string containing the command and its arguments.

        Usage:
        - destroy <class> <id> or <class>.destroy(<id>)
        """
        args = compare_blacket(arg)
        object_dictionary = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in object_dictionary.keys():
            print("** no instance found **")
        else:
            del object_dictionary["{}.{}".format(args[0], args[1])]
            storage.save()

    def perform_all(self, arg):
        """
        Print string representation of all instances of a
        class all instances specified.

        Parameters:
            - self: A reference to the current instance of the class.
            - arg: A string containing the command and its arguments.
        Usage:
            - all <class> or <class>.all()
        """
        args = compare_blacket(arg)
        if len(args) > 0 and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            name = []
            for obj in storage.all().values():
                if len(args) > 0 and args[0] == obj.__class__.__name__:
                    name.append(obj.__str__())
                elif len(args) == 0:
                    name.append(obj.__str__())
            print(name)

    def perform_create(self, arg):
        """
        Create a new instance of a specified class and print its identifier.

        Parameters:
        - self: A reference to the current instance of the class.
        - arg: The argument string provided with the create command.

        Returns:
        - None
        """
        parsed_args = compare_blacket(arg)
        if len(parsed_args) == 0:
            print("** class name missing **")
        elif parsed_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(parsed_args[0])().id)
            storage.save()

    def update_perform(self, arg):
        """
        Update a class instance of a given ID by adding or
        updating attribute key/value pairs or dictionary.

        Parameters:
        - self: A reference to the current instance of the class.
        - arg: A string containing the command and its arguments.

        Usage:
            - update <class> <id> <attribute_name> <attribute_value>
            - <class>.update(<id>, <attribute_name>, <attribute_value>)
            - <class>.update(<id>, <dictionary>)
         """
        args = compare_blacket(arg)
        object_dictionary = storage.all()

        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in object_dictionary.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(args) == 4:
            obj = object_dictionary["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                counter = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = counter(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif type(eval(args[2])) == dict:
            obj = object_dictionary["{}.{}".format(args[0], args[1])]
            for k, v in eval(args[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    counter = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = counter(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
