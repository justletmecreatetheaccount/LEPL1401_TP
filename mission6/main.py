from ast import arg
import random, requests, json, os, time, sys

def distance_h(string1, string2):
    strings = [string1.lower(), string2.lower()]
    strings.sort(key=lambda a: len(a))
    string1, string2 = strings
    d = len(string2) - len(string1)
    for (index, x) in enumerate(string1):
        d += 0 if string2[index] == x else 1
    
    return d

def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

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
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Assistant:
    def __init__(self, name):
        self.commands = {}
        self.words = {}
        self.fileName = None
        self.fileLines = 0
        self.fileChars = 0
        self.name = name
        self.jokes = []
        self.register_command("exit", None) #For fuzzy search

    def register_command(self, commandName, command, paramsNumber=0):
        
        self.commands[commandName] = (paramsNumber, command)



    def execute_command(self, commandName, args):
        
        if not commandName in self.commands.keys():
            return self.not_found(commandName)
        argsNumber, cmd = self.commands[commandName]
        if len(args) != argsNumber and argsNumber != -1:
            print(f"{bcolors.FAIL}{commandName} should take {argsNumber} arguments.{bcolors.ENDC}")
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
        suggestion = f"Did you mean {bcolors.OKCYAN}{bestMatch}{bcolors.OKBLUE}? " if len(bestMatch) > 0 and bestMatchV < 3 else ""
        self.speak(f"{suggestion}To see all commands, type 'help' ")
    
    def speak(self,*args):
        print(bcolors.OKBLUE, *args, bcolors.ENDC)
        if random.randint(0,100) > 90:
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
            char = getch().decode() 
            append = True
            if char == '\x03': #CTRL+C
                break 
            if char == '\x08': #Backspace
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
            color = bcolors.OKCYAN if validCommand else bcolors.FAIL
            
            cmdName = f'{color}{input[0]}{bcolors.ENDC}'

            argsPart = ""
            if not validCommand:
                argsPart = " ".join(input[1:])
            else:
                argsNumber = self.commands[input[0]][0]
                if argsNumber == -1:
                    argsNumber = len(input)
                blue = " ".join(input[1:argsNumber+1])
                red = " ".join(input[argsNumber+1:])
                argsPart = f'{bcolors.OKBLUE}{blue}{bcolors.ENDC}{" " if len(input) > argsNumber+1 and argsNumber > 0 else ""}{bcolors.FAIL}{red}{bcolors.ENDC}'

            line = '{startLine}{cmd}{space}{args}{whitespaces}'.format(
                startLine = startLine,
                cmd = cmdName,
                space = " " if len(input) > 1 else "",
                args= argsPart,
                whitespaces = " "*(max_length - length)
            )
            sys.stdout.write('\r'+ line)
    def run(self):
    
        self.speak(f"Bonjour! Je m'appelle {bcolors.OKCYAN}{self.name} {bcolors.ENDC}")
        while True:
            entry = self.get_user_input("--> ")
            command = entry[0]
            if command == "exit":
                break
            args = entry[1:]
            self.execute_command(command, args)
            
            
        print(f"{bcolors.WARNING}Goodbye !{bcolors.ENDC}")

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

    assistant.speak(f"""{bcolors.OKCYAN} Lines: {bcolors.OKBLUE} {assistant.fileLines}
 {bcolors.OKCYAN} Chars: {bcolors.OKBLUE} {assistant.fileChars}""")

def cmd_load_dico(assistant: Assistant, args):
    assistant.load_dictionnary()

def cmd_search(assistant: Assistant, args):
    if args[0] == "rick":
        rick()
        return
    present =  args[0] in assistant.words
    line = f'at line {bcolors.OKGREEN}{assistant.words.index(args[0])+1}{bcolors.OKBLUE} ' if present else ""
    assistant.speak(f"{bcolors.OKCYAN} {args[0]} {bcolors.OKBLUE}is {'not ' if not present else ''}in dictionary {line}")

def help(assistant: Assistant, args):

    assistant.speak(f"""
    Welcome to this guide !
    My name is {assistant.name} and i'm an useless bot :)
    Being useless does not mean that i can't do anything of course.
    
    Here is how you can interact with me:
    
    file <name>: Specify the file i'm currently looking at.
    info: Show informations about the file you specified (lines number and chars number)
    dictionary: Load specified file as a dictionnary
    search <word>: Lookup in dictionnary if your word is in it
    sum <number1> ... <numbern>: Compute sum of specified numbers (separated with spaces)
    avg <number1> ... <numbern>: Compute average of specified numbers (separated with spaces)
    help: Shows this message
    exit: Kills me. PLEASE don't do that. 
    
    """)
    

if __name__ == "__main__":
    johny = Assistant("Johny")
    johny.register_command("hello", hello)
    johny.register_command("file", cmd_set_file, paramsNumber=1)
    johny.register_command("info", file_info)
    johny.register_command("help", help)
    johny.register_command("dictionary", cmd_load_dico)
    johny.register_command("avg", avg, paramsNumber=-1) #-1 means infinite paramsNumber
    johny.register_command("sum", sum,  paramsNumber=-1)
    johny.register_command("search", cmd_search, paramsNumber=1)
    johny.jokes = [
        "La différence entre toi et moi ? Moi je fichier et toi tu fais chier"

    ]
    johny.run()

