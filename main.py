from subprocess import call
#First script using this instead of os.system() so this is probably garbage code


def Main(): #Main function
    print("Keep your device unplugged for now!")
    usb_or_wifi = get_input("USB connection or Wi-Fi [U/w]? ", ["u", "w"], "u")
    print("Killing any active ADB processes...")
    call(["pkill", "adb"]) #Kill ADB to prevent bugs
    additional_settings = get_input("Would you like to configure additional settings [y/N]? ", ["y", "n"], "n")
    cmd_line_param = []
    if additional_settings == "y": #Should we get additional settings?
        cmd_line_param = AdditionalSettings(usb_or_wifi)
        if usb_or_wifi == "w": #Specify port (WiFi only, might implement for USB some day)
            port = input("Specify custom port [5555]: ")
            if port == "":
                port = "5555"
    else:
        port = "5555"
   
    if usb_or_wifi == "w": #Run additional WiFi related things
        WiFi(port)
        useless_var = input("Unplug your phone, then press ENTER!")
    elif usb_or_wifi == "u":
        useless_var = input("Plug in your phone, then press ENTER!")
    else: #Not sure how we got here...
        print("Please report the error INVALID USB/WIFI VAR and specify the following value: " + answer)


    final_command = ["scrcpy"] #List for specifying the final command to be run by call
    for i in cmd_line_param:
        final_command.append(i) #Add additional parameters specified during additional settings (if any)
    command_to_user = ""
    for i in final_command:
        command_to_user = command_to_user + " " + i
    print(command_to_user) #These 3 lines print the end command that will be executed to the user. Makes life easier for debugging.
    call(final_command) #Here we are. The line that this whole program builds up to. Run scrcpy with parameters specified (if any)




def get_input(question, list_of_answers, default): #Accepts a question and a list of answers
    answer = input(question) #Asks the user the question
    answer = answer.lower() #Makes the answer lowercase
    if answer == "":
        print("")
        return default
    elif (answer not in list_of_answers) and (list_of_answers != []): #If the answer isn't in the list and the list isn't blank
        print("Invalid response!") #Declare response invalid
        get_input(question, list_of_answers) #Ask again
    else:
        print("") #Blank line for readability
        return answer #Return supplied answer
    
def AdditionalSettings(usb_or_wifi): #Possibly may re-work this code to use the function get_input
    cmd_line_param = []
    bitrate = input("Specify custom bitrate value [8M]: ") #specify bitrate
    if bitrate == "":
        bitrate = "8M"
    cmd_line_param.append("-b")
    cmd_line_param.append(bitrate)
    print("")
    max_size = input("Specify max screen resolution (only one number, see scrcpy documentation if you're confused) [0]: ") #Specify resolution
    if max_size == "":
        max_size = "0"
    cmd_line_param.append("-m")
    cmd_line_param.append(max_size)
    print("")
    if usb_or_wifi == "u":
        serial = input("Enter serial number of device (required if multiple devices connected!): ") #Specify serial number if multiple devices are connected to the computer (might break if connecting via wifi)
        if serial != "":
            cmd_line_param.append("-s")
            cmd_line_param.append(serial)
            print("")
    touches = get_input("Show physical touches? [y/N]: ", ["y", "n"], "n")
    if touches == "y": #Show physical touches?
        cmd_line_param.append("-t")
    full = get_input("Start in fullscreen mode? [y/N]: ", ["y", "n"], "n")
    if full == "y": #Start in fullscreen mode?
        cmd_line_param.append("-f")
    return cmd_line_param

def WiFi(port):
    phone_ip = input("Please enter your phone's IP address! ") #Request IP from user
    useless_var=input("Plug in your phone, then press ENTER!") #Plug in phone request to user
    call(["adb", "shell", "exit"]) #We need a connection through USB once before we can do WiFi (limitation of Android)
    ip_and_port = phone_ip + ":" + port #I can't do lists
    call(["adb", "tcpip", port]) #Put adb in tcpip mode
    call(["adb", "connect", ip_and_port]) #Connect through WiFi
    return



    

Main() #We have to start the program somewhere, right?
