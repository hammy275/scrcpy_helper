const { exec } = require('child_process');
var readline = require('readline-sync');

//exec('command here')

function get_input(question, list_of_answers, defanswer) { //Accepts a question and a list of answers
    answer = readline.question(question) //Asks the user the question
    //answer = answer.lower() //Makes the answer lowercase
    if (answer ===  "") {
        return defanswer
      }
    //elif (!(list_of_answers.indexOf(answer) >= 0) && (list_of_answers !== [])) { //If the answer isn't in the list and the list isn't blank
      else if ((!((list_of_answers.indexOf(answer)) >= 0)) && (list_of_answers !== [])) {
        console.log("Invalid response!") //Declare response invalid
        get_input(question, list_of_answers) //Ask again
      }
    else {
        return answer //Return supplied answer
      }
    }

function Main() { //Main function
    console.log("Keep your device unplugged for now!")
    var usb_or_wifi = get_input("USB connection or Wi-Fi [U/w]? ", ["u", "w"], "u")
    console.log("Killing any active ADB processes...")
    exec("pkill adb") //Kill ADB to prevent bugs
    var additional_settings = get_input("Would you like to configure additional settings [y/N]? ", ["y", "n"], "n")
    var cmd_line_param = 'scrcpy'
    if (additional_settings === "y"){ //Should we get additional settings?
        var final_command = AdditionalSettings(usb_or_wifi)
        if (usb_or_wifi === "w") { //Specify port (WiFi only, might implement for USB some day)
            var port = readline.question("Specify custom port [5555]: ")
            if (port === "") {
                port = "5555"
          }
      }
    }
    else{
        var port = "5555"
        var final_command = "scrcpy"
      }

    if (usb_or_wifi === "w") { //Run additional WiFi related things
        WiFi(port)
        var useless_var = readline.question("Unplug your phone, then press ENTER!")
      }
    else if (usb_or_wifi === "u"){
        var useless_var = readline.question("Plug in your phone, then press ENTER!")
      }
    console.log(final_command) //These 3 lines print the end command that will be executed to the user. Makes life easier for debugging.
    exec(final_command) //Here we are. The line that this whole program builds up to. Run scrcpy with parameters specified (if any)
}

function AdditionalSettings(usb_or_wifi){ //Possibly may re-work this code to use the function get_input
    var cmd_line_param = 'scrcpy'
    var bitrate = readline.question("Specify custom bitrate value [8M]: ") //specify bitrate
    if (bitrate === ""){
        bitrate = "8M"}
    cmd_line_param = cmd_line_param + " -b "
    cmd_line_param += bitrate
    var max_size = readline.question("Specify max screen resolution (only one number, see scrcpy documentation if you're confused) [0]: ") //Specify resolution
    if (max_size === "") {max_size = "0"}
    cmd_line_param += " -m "
    cmd_line_param += max_size
    if (usb_or_wifi === "u"){
        var serial = readline.question("Enter serial number of device (required if multiple devices connected!): ") //Specify serial number if multiple devices are connected to the computer (might break if connecting via wifi)
        if (serial !== ""){
            cmd_line_param += " -s "
            cmd_line_param += serial
          }}
    var touches = get_input("Show physical touches? [y/N]: ", ["y", "n"], "n")
    if (touches === "y"){ //Show physical touches?
        cmd_line_param += " -t "}
    var full = get_input("Start in fullscreen mode? [y/N]: ", ["y", "n"], "n")
    if (full === "y"){ //Start in fullscreen mode?
        cmd_line_param += " -f "}
    return cmd_line_param
  }

function WiFi(port){
    phone_ip = readline.question("Please enter your phone's IP address! ") //Request IP from user
    useless_var = readline.question("Plug in your phone, then press ENTER!") //Plug in phone request to user
    exec("adb shell exit") //We need a connection through USB once before we can do WiFi (limitation of Android)
    ip_and_port = phone_ip + ":" + port //I can't do lists
    exec("adb tcpip " + port) //Put adb in tcpip mode
    exec("adb connect " + ip_and_port) //Connect through WiFi
    return
  }





Main() //We have to start the program somewhere, right?
