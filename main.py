from subprocess import call
#First script using this instead of os.system() so this is probably garbage code

def GetUserInput():
    print("Keep your device unplugged for now!") 
    usb_or_wifi = input("USB connection or Wi-Fi [U/W]?") #User prompt to choose connection type
    call(["pkill", "adb"]) #Kill any instances of adb to prevent glithces    
    usb_or_wifi = usb_or_wifi.lower()
    if usb_or_wifi == "u": 
        AdditionalSettings(usb_or_wifi)
    elif usb_or_wifi == "w":
        AdditionalSettings(usb_or_wifi)
    else:
        print("Invalid option. We'll ask again :D") #Make sure the user actually made a proper selection as to not break code later
        print("")
        print("")
        GetUserInput()

def AdditionalSettings(usb_or_wifi): #User prompt to configure additional settings
    additional_settings = input("Would you like to configure additional settings [y/N]?")
    additional_settings = additional_settings.lower()
    if additional_settings == "y":
        #Additional settings
        ExtraSettingsSetup(usb_or_wifi) 
    else:
        InitConnectNoSetting(usb_or_wifi)

def InitConnectNoSetting(usb_or_wifi):
    cmd_line_param = []
    if usb_or_wifi == "u": #USB is so short we can just run it here
        USBConnect(cmd_line_param)
        return
    elif usb_or_wifi == "w":
        port = "5555"
        WiFiADB(cmd_line_param, port) #WiFi connectivity takes a bit more so it's in another function

def ExtraSettingsSetup(usb_or_wifi): #Extra parameters function for those who want it
    cmd_line_param = []
    bitrate = input("Specify custom bitrate value [8M]: ") #specify bitrate
    if bitrate == "":
        bitrate = "8M"
    cmd_line_param.append("-b")
    cmd_line_param.append(bitrate)
    max_size = input("Specify max screen resolution (only one number, see scrcpy documentation if you're confused) [0]: ") #Specify resolution
    if max_size == "":
        max_size = "0"
    cmd_line_param.append("-m")
    cmd_line_param.append(max_size)
    if usb_or_wifi == "w": #Specify port (WiFi only, might implement for USB some day)
        port = input("Specify custom port [5555]: ")
        if port == "":
            port = "5555"
    if usb_or_wifi == "u":
        serial = input("Enter serial number of device (required if multiple devices connected!): ") #Specify serial number if multiple devices are connected to the computer (might break if connecting via wifi)
        if serial != "":
            cmd_line_param.append("-s")
            cmd_line_param.append(serial)
    touches = input("Show physical touches? [y/N]: ")
    touches = touches.lower()
    if touches == "y": #Show physical touches?
        cmd_line_param.append("-t")
    if usb_or_wifi == "u":
        USBConnect(cmd_line_param)
    elif usb_or_wifi == "w":
        WiFiADB(cmd_line_param, port)

def USBConnect(cmd_line_param):
    useless_var = input("Plug in your phone, then press ENTER!")
    TheFinalRun(cmd_line_param)

def WiFiADB(cmd_line_param, port):
    phone_ip = input("Please enter your phone's IP address! ") #Request IP from user
    useless_var=input("Plug in your phone, then press ENTER!") #Plug in phone request to user
    call(["adb", "shell", "exit"]) #We need a connection through USB once before we can do WiFi (limitation of Android)
    ip_and_port = phone_ip + ":" + port #I can't do lists
    call(["adb", "tcpip", port]) #Put adb in tcpip mode
    call(["adb", "connect", ip_and_port]) #Connect through WiFi
    useless_var=input("Unplug your device from the USB port, then press ENTER to continue") #Unplug!
    TheFinalRun(cmd_line_param)
    
def TheFinalRun(cmd_line_param): #Whether we're going through USB or Wi-Fi, with or without custom settings, everything leads here
    final_command = ["scrcpy"] #List for specifying the final command to be run by call
    for i in cmd_line_param:
        final_command.append(i) #Add additional parameters specified during additional settings (if any)
    command_to_user = ""
    for i in final_command:
        command_to_user = command_to_user + " " + i
    print(command_to_user) #These 3 lines print the end command that will be executed to the user. Makes life easier for debugging.
    call(final_command) #Here we are. The line that this whole program builds up to. Run scrcpy with parameters specified (if any)

GetUserInput() #We have to start the program somewhere, right?
