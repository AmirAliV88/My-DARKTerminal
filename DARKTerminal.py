import os, psutil, numpy, getpass, platform

# color set
if os.name == "nt":
   n = ""
   r = ""
   g = ""
   p = ""
   b = "" 
   # colors is not undfind on Windows
else:
   n = "\033[0m"
   r = "\033[31m"
   g = "\033[32m"
   p = "\033[35m"
   b = "\033[36m"   
   # font colors on Linux and AppleMAc

print(f"{n}Terminal Shell: {n}")

command_runner = True
Adminstor_action = False
backinput = f"{g}>__/: {n}"

def getSysteminfo():
   systeminfo = f'''{b}
 OS Name: {platform.system()}
 OS Release: {platform.release()}
 User: {platform.node()}
 Machine: {platform.machine()}
 Current Path: {os.getcwd()}
   {n}'''
   return systeminfo

commandlists = [
	("help", "this page"), ("system", "showing system informations"),
	("echo", "print your text"), ("battery", "check your battery"),
	("cd", "change the path and go every whrere in the directorys")
]


def Adminstor(args):
   global backinput, Adminstor_action
   if Adminstor_action: backinput = f"{g}>__/: {n}"; Adminstor_action = False
   else:
      enterpass = getpass.getpass("Enter Adminstor password: ")
      if enterpass == "$.password": backinput = f"{r}>__/$: {n}"; Adminstor_action = True
      else: print(f"{r}Your are not Adminstor {n}")


def runscript(filepath):

   doctype = "<DARK script>"
   start_script_line = None
   filepath_array = filepath.split(".")

   def readerscript(filepath):
      if filepath_array[len(filepath_array)-1:] != ["dtx"]: return None
      try:
         with open(filepath, 'r', encoding='utf-8') as file:
            start_script_line = None
            for line_number, line in enumerate(file, start=1):
               if doctype in line: 
                  start_script_line = line_number+1
            return start_script_line
      except FileNotFoundError: print(f"Error: file '{filepath}' not found"); return None

   def runner(filepath, start_line):
      with open(filepath, 'r', encoding='utf-8') as file: lines = file.readlines()
      if start_line < 1: start_line = 1
      elif start_line > len(lines): start_line = "MAX"
      scriptcommands = ''.join(lines[start_line-1:]).replace("\n",'').split(";")
      for scmd in scriptcommands:
         scmdo = scmd.split(" ")
         if scmdo[0] != "//" and scmdo[0] != "":
            run_command_line(scmd, scmd.split(" "))

   start_script_line = readerscript(filepath)
   if start_script_line != None: runner(filepath, start_script_line)
   else: print("Error: script file don't started any dark script")


# main method
def run_command_line(cmd, cmdo):
   match cmdo[0]:

      case "help":
         printhelp = ""
         for c,d in commandlists: 
            printhelp += f"{p} {c}: {d}{b}\n"
            print("\n"+printhelp)

      case "system": print(systeminfo) 

      case "echo": print(' '.join(cmdo[1:]))

      case "battery":
         battery = psutil.sensors_battery()
         if battery is None: print("No battery detected.")
         battery_percent = battery.percent
         print(f"{p}Current battery percentage: {numpy.round(battery_percent, decimals=1)}%{n}")

      case "clear": 
         clearcmd = "cls" if os.name=="nt" else "clear"
         os.system(clearcmd)

      case "cd":
         try: os.chdir(cmdo[1]); print(b, os.getcwd(), n)
         except IndexError: print(b, os.getcwd(), n)

      case "$": Adminstor(cmdo)
      case "!$": Adminstor_action = True; Adminstor(cmdo)
      case "!": Adminstor_action = True; Adminstor(cmdo)
      # case "$?": #help for adminstor: publish_help + admin_help

      case "runscript": runscript(cmdo[1])

      # Error
      case cmd: print(f"{r}Error: command {cmd} is not defind{n}")

# main runner
while command_runner: 
   cmd = input(backinput)
   cmd = cmd.lower()
   cmdo = cmd.split(" ")
   run_command_line(cmd, cmdo)

