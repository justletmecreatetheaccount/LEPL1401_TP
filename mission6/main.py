from http.client import responses
import random, json, os, time, sys
try : import requests
except Exception as e: 
    print ("This message should be replaced by a requirements.txt but we couldn't give you one, so here is an ugly message instead.")
    print("You need 'requests' module installed ")
    print(e)
    sys.exit(1)


"""
======
Program variables
======
"""
NEWS_API_KEY="a3cfdcbd372a498b982bd2fcde1592b6"
TRANSLATE_API_KEY="8d9932ce-70a6-5a26-63ad-686a2e7dc067:fx"


"""
=====
Utils (colors, terminal stuff)
=====

"""
class TerminalLine:
    """
    This class is usefull to edit a printed line to the terminal.
    Usage:
        TerminalLine.new_line(content) --> Will print content
        TerminalLine.set_line_content(content) --> Will edit the last printed content with content
    """
    length = 0
    def new_line(content):
        sys.stdout.write(content)
        sys.stdout.flush()
        TerminalLine.length = len(content)
    def set_line_content(content):
        sys.stdout.write('\r'+TerminalLine.length * " ") #Erase the line before writing on it
        sys.stdout.write('\r'+ content)
        TerminalLine.length = len(content)

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
    This function return a function getch, this function is like input in python, but instead of waiting user to type a line then enter, it'll wait and return next user CHAR type.

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
    BOLD = '\033[1m'

def color(text, bcolor, end=bcolors.ENDC):
    """
    Will return a string with colored text
    """
    return f"{bcolor}{text}{end}"

"""
=====
Principal assistant code
=====

"""

class Assistant:
    def __init__(self, name):
        self.commands = {}
        self.words = {}
        self.fileName = None
        self.fileLines = 0
        self.fileChars = 0
        self.name = name
        self.register_command("exit", None, description="Kills me. Please don't do that") #For fuzzy search. The exit behavior is in run()

    def register_command(self, commandName, command, paramsNumber=0, description=""):
        """
        This function register a new command in the assistant.
        """
        self.commands[commandName] = (paramsNumber, command, description)



    def execute_command(self, commandName, args):

        if not commandName in self.commands.keys():
            return self.not_found(commandName)

        argsNumber, cmd, _ = self.commands[commandName]

        if len(args) != argsNumber and argsNumber != -1:
            if argsNumber == 0:
                print(color(f"{commandName} should not take any arguments.", bcolors.RED))
            else:
                print(color(f"{commandName} should take {argsNumber} arguments.", bcolors.RED))
            return

        try:
            cmd(self, args)
        except Exception as e:
            print(f"An error occured while executing {cmd}:", color(e, bcolors.RED))
            
    
    def not_found(self, command):
        """
        Code executed when running invalid command like "sim" or "jakkabab"
        """
        bestMatch = ""
        bestMatchV = 10
        for c in self.commands.keys():
            distance = distance_h(c, command)
            if distance <= bestMatchV:
                bestMatch = c
                bestMatchV = distance
        suggestion = ""
        if len(bestMatch) > 0 and bestMatchV < 3:
            suggestion = f"Did you mean {color(bestMatch, bcolors.CYAN, end=bcolors.BLUE)}? "
        self.speak(f"{suggestion}To see all commands, type 'help' ")
    
    def speak(self,text):
        print(bcolors.BLUE, text, bcolors.ENDC)

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
                    self.speak(f"{color(f'Invalid file format (file: {self.fileName})', bcolors.RED)}")
                    f.close()
                    return
                tmp_words.append(tokens[0])
            self.words = tmp_words
        self.speak("Words loaded !")

    def get_user_input(self, startLine):
        """
        The most complicated function of this file.
        This function is charged of the user-prompt.

        Args:
        startLine: prompt format (prefix of user input) (string) 
        """

        input = [""] #Contain user input like [commandName, arg1, arg2, ...]
        input_index = 0
        getch = _find_getch()
        TerminalLine.new_line(startLine)

        while True: #Wait for user to type chars
            try:
                char = getch()
            except UnicodeDecodeError:
                continue

            append = True

            if char == '\x03': #CTRL+C
                print()
                return ["exit"] 

            if char == '\x08' or char == '\x7f': #Backspace
                if len(input[input_index]) == 0:
                    if input_index == 0:
                        continue
                    input_index -= 1
                    input = input[:-1]
                input[input_index] = input[input_index][:-1]
                append = False

            if char == '\r' or char == '\n': # Enter pressed
                print()
                return [x for x in input if len(x) > 0] #Returning all non-empty args (to avoid empty args because of spaces)
            
            if char == " ": #When space is pressed, we have to add another value in input
                input_index += 1
                input.append("")
                append = False
            if append:
                input[input_index] += char

            """
            The part below is only the coloring of user input
            """
            isValidCommand =  input[0] in self.commands.keys()

            cmd_color = bcolors.CYAN if isValidCommand else bcolors.RED
            
            cmdName = color(input[0], cmd_color)

            argsPart = ""

            if not isValidCommand:
                argsPart = " ".join(input[1:])
            else:
                """
                Color in blue the first x arguments corresponding to command args number.
                """
                argsNumber = self.commands[input[0]][0]
                if argsNumber == -1:
                    argsNumber = len(input)
                blue = " ".join(input[1:argsNumber+1])
                red = " ".join(input[argsNumber+1:])
                argsPart = f'{color(blue, bcolors.BLUE)}{" " if len(input) > argsNumber+1 and argsNumber > 0 else ""}{color(red, bcolors.RED)}'

            """
            Updating line with colors
            """
            line = '{startLine}{cmd}{space}{args}'.format(
                startLine = startLine,
                cmd = cmdName,
                space = " " if len(input) > 1 else "",
                args= argsPart,
            )
            TerminalLine.set_line_content(line)

    def run(self):
        """
        Main function of assistant
        """
        self.speak(f"Hi ! My name is {color(self.name, bcolors.YELLOW, end=bcolors.BLUE)}.")
        self.speak(f"Don't hesitate to run {color('help', bcolors.CYAN, end=bcolors.BLUE)} to know what i'm capable of !")
        while True:
            entry = self.get_user_input("--> ")
            command = entry[0]
            if command == "exit":
                break
            args = entry[1:]
            self.execute_command(command, args)
            
            
        print(color("Goodbye.", bcolors.YELLOW))

"""
=====
Commands code
=====

"""
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
        time.sleep(1/7)
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
    line = f'at line {bcolors.GREEN}{assistant.words.index(args[0])+1}{bcolors.BLUE} ' if present else ""
    assistant.speak(f"{bcolors.CYAN} {args[0]} {bcolors.BLUE}is {'not ' if not present else ''}in dictionary {line}")
    
def weather(assistant: Assistant, args):
    url = f"https://wttr.in/{' '.join(args) if len(args) > 0 else ''}"
    u = requests.get(url)
    assistant.speak(u.text)

def news(assistant: Assistant, args):
    dat = None
    if len(args)>0:
        dat = requests.get(f"https://newsapi.org/v2/everything?q={' '.join(args)}&apiKey="+NEWS_API_KEY)
    else:
        dat = requests.get("https://newsapi.org/v2/top-headlines?country=fr&apiKey="+NEWS_API_KEY)
    articles = json.loads(dat.text)["articles"][:5]
    for article in articles:
        source = article["source"]["name"]
        author = article["author"]
        title = article["title"]
        desc = article["description"]
        url = article["url"]
        text = f"""
{color(color(title, bcolors.RED), bcolors.BOLD)}   
{color(source, bcolors.YELLOW)} - {color(author, bcolors.CYAN)} - {url}
{desc}
        """
        assistant.speak(text)
    
def translate(assistant: Assistant, args):
    if len(args) < 3:
        assistant.speak(color("Three args are needed !", bcolors.RED))
        return
    if not  (len(args[0]) == 2 and len(args[1]) == 2):
        assistant.speak(color("The two first arguments have to be language code like en, fr, ..."))
    headers = {
    'Authorization': 'DeepL-Auth-Key '+TRANSLATE_API_KEY,
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'text={" ".join(args[2:])}&target_lang={args[1].upper()}&source_lang={args[0].upper()}'

    response = requests.post('https://api-free.deepl.com/v2/translate', headers=headers, data=data)
    try:
        translations = json.loads(response.text)["translations"]
    except KeyError:
        assistant.speak("No translations found.")
        return
    assistant.speak(color(f'{translations[0]["text"]}', bcolors.YELLOW))

def music(assistant: Assistant, args):
    musics = ["KuC7FFdIaQg", "U-MIsGy9V5w", "Kt0MtjnuScY"]
    assistant.speak(f"Here is my music of the moment: https://youtube.com/watch?v={random.choice(musics)}")

def help(assistant: Assistant, args):

    descriptions = []
    for x in assistant.commands.keys():
        args = assistant.commands[x][0] or 0
        desc = assistant.commands[x][2]
        descriptions.append("{commandName}: {commandDescription} {args}".format(
            commandName = color(x, bcolors.CYAN),
            commandDescription = desc,
            args= color(f"({args} arg{'s' if args > 1 else ''})", bcolors.RED) if args > 0 else ("" if args == 0 else color("(Any args number you want)", bcolors.RED))
        ))
    description = "\n".join(descriptions)
    assistant.speak(f"""
Welcome to this guide !
My name is {color(assistant.name, bcolors.YELLOW, end=bcolors.BLUE)} and i'm an useless bot :)
Being useless does not mean that i can't do anything, of course.

Here is how you can interact with me (there's a little bonus, try {color('search rick', bcolors.YELLOW, end=bcolors.BLUE)}):

{description}
    """)

    

if __name__ == "__main__":
    assistant = Assistant(random.choice(["Mallory","Alfred","Neo","Philibert","Tchoupi"]))
    assistant.register_command("hello", hello, description="A simple test command that prints Hello World.")
    assistant.register_command("file", cmd_set_file, paramsNumber=1, description="Command that specify the file the program is looking at.")
    assistant.register_command("info", file_info, description="Show informations (lines and chars numbers) about selected file.")
    assistant.register_command("help", help, description="Show this message.")
    assistant.register_command("words", cmd_load_dico, description="Load the file as a word list (used by search cmd).")
    assistant.register_command("avg", avg, paramsNumber=-1, description="Compute the average value of args.") #-1 means infinite paramsNumber
    assistant.register_command("sum", sum,  paramsNumber=-1, description="Compute the sum of args.")
    assistant.register_command("search", cmd_search, paramsNumber=1, description="Search a word inside the dictionary.")
    assistant.register_command("weather", weather, paramsNumber=-1, description="Get the weather, specify a city if you want, or it'll be based on your IP.")
    assistant.register_command("clear", lambda assistant,args: clear_screen(), paramsNumber=0, description="Clear the screen.")
    assistant.register_command("news", news, paramsNumber=-1, description="A command to get worldwide news. You can specify args to search for specific topics.")
    assistant.register_command("translate", translate, paramsNumber=-1, description="<from_lg> <to_lg> text --> Translate text from a language to another language. You have to put languages codes like en, fr, ru, ...")
    assistant.register_command("music", music, paramsNumber=0, description="Show my music of the moment !")
    assistant.run()

