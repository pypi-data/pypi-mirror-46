# By Seth Peace

from . import keyboard
import time, clear_screen

def print_tool(title, options, selected_option):
    
    index = 1

    print(title, "\n---")
    
    for option in options:
        if(selected_option == index):
            print("(•)", option)
            
        else:
            print("(", index, ") ", option, sep="")
            
        index += 1

def menu(title   =  "DEFAULT MENU",
         options = ["DEFAULT OPTION 1",
                    "DEFAULT OPTION 2",
                    "DEFAULT OPTION 3",
                    "DEFAULT OPTION 4",
                    "DEFAULT OPTION 5"]):
    
    no_change       = True
    selected_option = 1
    
    while(True):
        
        clear_screen.clear()
        print_tool(title, options, selected_option)
        
        if(keyboard.is_pressed("up") and selected_option > 1):
            selected_option -= 1
            
        elif(keyboard.is_pressed("down") and selected_option < len(options)):
            selected_option += 1

        elif(keyboard.is_pressed("enter")):
            break

        time.sleep(0.1)
        
    return selected_option
