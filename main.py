from subprocess import call
import sys

port = "5555"

def main():
    global port
    """Asks the user questions and uses the answers
    to do things in other functions accordingly"""
    print("Unplug your device now!!")
    connection_type = get_input("Connect through USB or WiFi? [U/w]", ["u", "w"], "u")
    print("Killing adb, just in case.")
    run(["adb", "kill-server"])
    command = additional_settings(connection_type)
    if connection_type == "w":
        phone_ip = input("Please enter your phone's IP address! ")
        input("Plug in your phone, then press ENTER!")        
        run(["adb", "shell", "exit"])
        ip_and_port = phone_ip + ":" + port
        run(["adb", "tcpip", port])
        run(["adb", "connect", ip_and_port]) #Connect through WiFi
        input("Unplug your phone, then press ENTER!")
    else:
        input("Plug your phone in, then press ENTER!")
    print("Running: "+ " ".join(command))
    run(command)

def additional_settings(type):
    """Asks the user questions about an
    optional set of questions. If they
    agree, ask them.
    Returns command: A list containing
    everything that will be run at the end
    of the program.
    Globals port when WiFi is in use."""
    command = ["scrcpy"]
    settings = get_input("Would you like to configure additional settings? [y/N]", ["y", "n"], "n")
    if settings == "n":
        return command
    command.append("-b")
    command.append(get_input("Specify custom bitrate [8M]: ", [], "8M"))
    command.append("-m")
    command.append(get_input("Specify screen resolution [0]: ", [], "0"))
    if type == "u":
        serial = get_input("Input device serial number; if applicable: ", [], "")
        if serial != "":
            command.append("-s")
            command.append(serial)
    if type == "w":
        global port
        port = get_input("Enter a port to use for communications [5555]", [], "5555")
    if get_input("Start in fullscreen mode? [y/N]", ["y", "n"], "n") == "y":
        command.append("-f")
    if get_input("Show physical touches? [y/N]", ["y", "n"], "n") == "y":
        command.append("-t")
    return command

    

def get_input(question, answers, default):
    """Prompts user a question with acceptable answers.
    Returns an acceptable answer"""
    answer = " "
    while (answer != "" and not answer in answers) or (answers == [] and answer == " "):
        answer = input(question)
    if answer == "":
        return default
    return answer

def run(command):
    """Runs a command and errors out
    if it fails"""
    try:
        call(command)
    except:
        print('Error running command: ' + " ".join(command))
        sys.exit(1)

if __name__ == "__main__":
    main()