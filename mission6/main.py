import random, json, os, time, sys
from datetime import datetime
try : import requests
except : 
    print ("afin de beneficier de toutes mes capacités veuillez intaller le module requests")
    sys.exit(1)
    


def distance_h(string1, string2):
    """
    This function computes distance between two strings, usefull for fuzzy command search (sim --> sum)
    """
    strings = [string1.lower(), string2.lower()]
    strings.sort(key=lambda a: len(a))
    string1, string2 = strings
    d = len(string2) - len(string1)
    for (index, x) in enumerate(string1):
        d += 0 if string2[index] == x else 1
    
    return d

def _find_getch():
    """
    This function return a function getch, this function is like input in python, but instead of waiting user to type a line then enter, it'll return any char the user
    will type.

    This _find_getch is necessary because getch is not the same on linux and windows...
    """
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return lambda : msvcrt.getch().decode()

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

class bcolors:
    """
    Colors special chars for terminal
    """
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def color(text, bcolor, end=bcolors.ENDC):
    """
    Will return a string with colored text
    """
    return f"{bcolor}{text}{end}"

class Assistant:
    def __init__(self, name):
        self.commands = {}
        self.words = {}
        self.fileName = None
        self.fileLines = 0
        self.fileChars = 0
        self.name = name
        self.jokes = []
        self.register_command("exit", None, description="Kills me. Please don't do that") #For fuzzy search

    def register_command(self, commandName, command, paramsNumber=0, description=""):
        
        self.commands[commandName] = (paramsNumber, command, description)



    def execute_command(self, commandName, args):
        
        if not commandName in self.commands.keys():
            return self.not_found(commandName)
        argsNumber, cmd, desc = self.commands[commandName]
        if len(args) != argsNumber and argsNumber != -1:
            print(color(f"{commandName} should take {argsNumber} arguments.", bcolors.RED))
            return
        try:
            cmd(self, args)
        except Exception as e:
            print(f"An error occured while executing {cmd}:", e)
            
    
    def not_found(self, command):
        bestMatch = ""
        bestMatchV = 10
        for c in self.commands.keys():
            distance = distance_h(c, command)
            if distance <= bestMatchV:
                bestMatch = c
                bestMatchV = distance
        suggestion = f"Did you mean {color(bestMatch, bcolors.CYAN, end=bcolors.BLUE)}? " if len(bestMatch) > 0 and bestMatchV < 3 else ""
        self.speak(f"{suggestion}To see all commands, type 'help' ")
    
    def speak(self,*args):
        print(bcolors.BLUE, *args, bcolors.ENDC)
        if random.randint(0,100) > 99:
            print(random.choice(self.jokes))

    def set_file(self, fileName):
        
        with open(fileName) as f:
            content = f.read()
            self.fileChars = len(content)
            self.fileLines = len(content.split("\n"))
        self.fileName = fileName
        self.speak("File loaded !")
        
    def load_dictionnary(self):
        with open(self.fileName) as f:
            content = f.readlines()
            tmp_words = []
            for line in content:
                tokens = line.split(",")
                if len(tokens) > 2:
                    print("Invalid dictionnary format")
                    f.close()
                    return
                tmp_words.append(tokens[0])
            self.words = tmp_words
        self.speak("Dictionary loaded !")

    def get_user_input(self, startLine):
        max_length = 0
        input = [""]
        input_index = 0
        getch = _find_getch()
        sys.stdout.write('\r'+ startLine)
        while True:
            try:
                char = getch()
            except UnicodeDecodeError:
                continue
            append = True
            if char == '\x03': #CTRL+C
                break 
            if char == '\x08' or char == '\x7f': #Backspace
                if len(input[input_index]) == 0:
                    if input_index == 0:
                        continue
                    input_index -= 1
                    input = input[:-1]
                input[input_index] = input[input_index][:-1]
                append = False
            if char == '\r' or char == '\n':
                print()
                return input
            if char == " ":
                input_index += 1
                input.append("")
                append = False
            if append:
                input[input_index] += char
            length = len(" ".join(input))
            if length > max_length:
                max_length = length
            
            validCommand =  input[0] in self.commands.keys()
            t_color = bcolors.CYAN if validCommand else bcolors.RED
            
            cmdName = color(input[0], t_color)

            argsPart = ""
            if not validCommand:
                argsPart = " ".join(input[1:])
            else:
                argsNumber = self.commands[input[0]][0]
                if argsNumber == -1:
                    argsNumber = len(input)
                blue = " ".join(input[1:argsNumber+1])
                red = " ".join(input[argsNumber+1:])
                argsPart = f'{color(blue, bcolors.BLUE)}{" " if len(input) > argsNumber+1 and argsNumber > 0 else ""}{color(red, bcolors.RED)}'

            line = '{startLine}{cmd}{space}{args}'.format(
                startLine = startLine,
                cmd = cmdName,
                space = " " if len(input) > 1 else "",
                args= argsPart,
            )
            sys.stdout.write('\r'+len(line)*" " +  " "*(max_length - length))
            sys.stdout.write('\r'+ line)
    def run(self):
    
        self.speak(f"Bonjour! Je m'appelle {color(self.name, bcolors.CYAN)}")
        while True:
            entry = self.get_user_input("--> ")
            command = entry[0]
            if command == "exit":
                break
            args = entry[1:]
            self.execute_command(command, args)
            
            
        print(color("Goodbye.", bcolors.YELLOW))

#Commands code

def hello(assistant: Assistant, args):
    assistant.speak(f"Hello World ! My name is {assistant.name}")


def sum(assitant: Assistant, args, show=True):
    tot_sum = 0
    for i in args:
        try:
            tot_sum += float(i)
        except ValueError:
           raise ValueError("I don't like algebra stop with letters in math !")
    assitant.speak(tot_sum) if show else None
    return(tot_sum)


def rick():
    u = requests.get("https://theo.daron.be/dat.json")
    data = json.loads(u.text)
    for x in data:
        clear_screen()
        print(x)
        time.sleep(1/5)
    time.sleep(1)


def avg(assistant: Assistant, args):
    tot_sum = sum(assistant, args, show=False)
    assistant.speak(tot_sum / len(args))

def clear_screen():
    if(os.name == 'posix'):
       os.system('clear')
    # else screen will be cleared for windows
    else:
       os.system('cls')


def cmd_set_file(assistant: Assistant, args):

    assistant.set_file(args[0])
    

def file_info(assistant: Assistant, args):

     assistant.speak(f"""{color('Lines', bcolors.CYAN, end=bcolors.BLUE)} {assistant.fileLines}
 {color('Chars', bcolors.CYAN, end=bcolors.BLUE)} {assistant.fileChars}""")


def cmd_load_dico(assistant: Assistant, args):
    assistant.load_dictionnary()

def cmd_search(assistant: Assistant, args):
    if args[0] == "rick":
        rick()
        return
    present =  args[0] in assistant.words
    line = f'at line {bcolors.OKGREEN}{assistant.words.index(args[0])+1}{bcolors.OKBLUE} ' if present else ""
    assistant.speak(f"{bcolors.OKCYAN} {args[0]} {bcolors.OKBLUE}is {'not ' if not present else ''}in dictionary {line}")
    
def weather(assistant: Assistant, args):
    url = f"https://wttr.in{'/'+' '.join(args) if len(args) > 0 else ''}"
    u = requests.get(url)
    assistant.speak(u.text)


def help(assistant: Assistant, args):

    descriptions = []
    for x in assistant.commands.keys():
        descriptions.append( f"{color(x, bcolors.CYAN)}: {assistant.commands[x][2]}")
    description = "\n    ".join(descriptions)
    assistant.speak(f"""
    Welcome to this guide !
    My name is {assistant.name} and i'm an useless bot :)
    Being useless does not mean that i can't do anything of course.
    
    Here is how you can interact with me:

    {description}


    """)

    

if __name__ == "__main__":
    johny = Assistant("Johny")
    johny.register_command("hello", hello, description="A simple test command that prints Hello World")
    johny.register_command("file", cmd_set_file, paramsNumber=1, description="Command that specify the file the program is looking at")
    johny.register_command("info", file_info, description="Show informations (lines and chars numbers) about selected file")
    johny.register_command("help", help, description="Show this message")
    johny.register_command("dictionary", cmd_load_dico, description="Load the file as a dictionary (used by search cmd)")
    johny.register_command("avg", avg, paramsNumber=-1, description="avg <nbr_1>...<nbr_n> --> compute the average value of args") #-1 means infinite paramsNumber
    johny.register_command("sum", sum,  paramsNumber=-1, description="sum <nbr_1>...<nbr_n> --> compute the sum of args")
    johny.register_command("search", cmd_search, paramsNumber=1, description="Search a word inside the dictionary")
    johny.register_command("weather", weather, paramsNumber=-1, description="Get the weather, specify a city if you want, or it'll be based on your IP")
    johny.jokes = [
        "La différence entre toi et moi ? Moi je fichier et toi tu fais chier",
        "ça fait quoi d'être aussi utile qu'internet explorer ?"

    ]
    johny.run()

