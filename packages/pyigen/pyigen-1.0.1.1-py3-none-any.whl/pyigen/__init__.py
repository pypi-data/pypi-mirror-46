import time
import pkg_resources
name = "pyigen"

#pyigen.run() variables:
    #for no icon, make icon=None
    #console: True if u want console, False if u don't want console
    #pygameusage: if u want pygame, make True, False, if u don't want quit

slash=' \ '
def run(appname,filename,pygameusage,console,icon):

    print("Copy and Paste the code and run it in")
    print("the Terminal or your Command Prompt")
    print("in the same directory as",filename)
    print()
    print("Note: if you need to add a module, add '--hiddenimport modulename'")
    print()

    print("pyinstaller --onefile",end=' ')
    if console==False:
        print("-w", end=' ')
    if icon !=None:
        print("-i",icon, end=' ')

    if pygameusage==True:
        print("--hiddenimport pygame", end=' ')
    print(filename, end=' ')
        



def pyigen_license():
    lf=pkg_resources.resource_filename('pyigen','files/LICENSE-for-function.txt')

    with open(lf) as l: # The with keyword automatically closes the file when you are done
        print (l.read())
def manual():
    lfa=pkg_resources.resource_filename('pyigen','files/manual.txt')
    
    with open(lfa) as m: # The with keyword automatically closes the file when you are done
        print (m.read())

def about():
    print("About pyigen 1.0.1.1")
    print()
    print("Created by Armaan Aggarwal on May 15, 2019")

print("pyigen 1.0.1 successfully imported")
print("To see the manual of pyigen 1.0.1.1, use the command 'pyigen.manual()'")

