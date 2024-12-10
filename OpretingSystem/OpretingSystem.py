import os
import pyttsx3

class CustomOS:
    def __init__(self):
        self.users = {"123": "123"}  # Predefined user credentials
        self.current_user = None
        self.processes = []  # Simulated process list
        self.speaker = pyttsx3.init()  # Initialize text-to-speech engine
        voices = self.speaker.getProperty('voices')
        self.speaker.setProperty('voice', voices[0].id)  # 0 for male, 1 for female
        self.speaker.setProperty('volume', 0.8)  # Range: 0.0 (min) to 1.0 (max)



    def speak(self, text):
        """Speak the given text."""
        self.speaker.say(text)
        self.speaker.runAndWait()

    def welcome_message(self):
        message = "Welcome to Custom Operating System Simulation!"
        print(message)
        self.speak(message)
        print("Type 'help' to see available commands.")
        print("-" * 40)

    def authenticate(self):
        print("\nLogin to continue.")
        username = input("Username: ")
        password = input("Password: ")
        
        if username in self.users and self.users[username] == password:
            self.current_user = username
            message = f"Login successful! Welcome, {username}."
            print(message)
            self.speak(message)
        else:
            message = "Invalid credentials. Exiting..."
            print(message)
            self.speak(message)
            exit()

    def help_menu(self):
        print("\nAvailable Commands:")
        print("1. `createfile <filename>` - Create a new file")
        print("2. `deletefile <filename>` - Delete a file")
        print("3. `listfiles` - List all files in the current directory")
        print("4. `startprocess <process_name>` - Start a process")
        print("5. `stopprocess <process_name>` - Stop a process")
        print("6. `listprocesses` - List all running processes")
        print("7. `adduser <username> <password>` - Add a new user (123 only)")
        print("8. `logout` - Logout of the system")
        print("9. `exit` - Exit the simulation")

    def create_file(self, filename):
        self.speak(f"Creating file {filename}")
        if os.path.exists(filename):
            print(f"File '{filename}' already exists.")
            self.speak(f"File {filename} already exists.")
        else:
            with open(filename, 'w') as f:
                f.write("")  # Create an empty file
            print(f"File '{filename}' created on your computer.")
            self.speak(f"File {filename} created successfully.")

    def delete_file(self, filename):
        self.speak(f"Deleting file {filename}")
        if os.path.exists(filename):
            os.remove(filename)
            print(f"File '{filename}' deleted.")
            self.speak(f"File {filename} deleted.")
        else:
            print(f"File '{filename}' does not exist.")
            self.speak(f"File {filename} does not exist.")

    def list_files(self):
        self.speak("Listing all files in the current directory")
        files = os.listdir()
        if files:
            print("Files in the current directory:")
            for file in files:
                print(f"- {file}")
        else:
            print("No files found in the current directory.")
            self.speak("No files found in the current directory.")

    def start_process(self, process_name):
        self.speak(f"Starting process {process_name}")
        if process_name in self.processes:
            print(f"Process '{process_name}' is already running.")
            self.speak(f"Process {process_name} is already running.")
        else:
            self.processes.append(process_name)
            print(f"Process '{process_name}' started.")
            self.speak(f"Process {process_name} started.")

    def stop_process(self, process_name):
        self.speak(f"Stopping process {process_name}")
        if process_name in self.processes:
            self.processes.remove(process_name)
            print(f"Process '{process_name}' stopped.")
            self.speak(f"Process {process_name} stopped.")
        else:
            print(f"Process '{process_name}' is not running.")
            self.speak(f"Process {process_name} is not running.")

    def list_processes(self):
        self.speak("Listing all running processes")
        if self.processes:
            print("Running Processes:")
            for process in self.processes:
                print(f"- {process}")
        else:
            print("No processes are currently running.")
            self.speak("No processes are currently running.")

    def add_user(self, username, password):
        self.speak(f"Adding user {username}")
        if self.current_user == "admin":
            if username in self.users:
                print(f"User '{username}' already exists.")
                self.speak(f"User {username} already exists.")
            else:
                self.users[username] = password
                print(f"User '{username}' added successfully.")
                self.speak(f"User {username} added successfully.")
        else:
            print("Only 'admin' can add new users.")
            self.speak("Only admin can add new users.")

    def logout(self):
        self.speak(f"Logging out {self.current_user}")
        print(f"Goodbye, {self.current_user}!")
        self.current_user = None
        self.authenticate()

    def command_handler(self, command):
        parts = command.split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if cmd == "help":
            self.help_menu()
        elif cmd == "createfile" and args:
            self.create_file(args[0])
        elif cmd == "deletefile" and args:
            self.delete_file(args[0])
        elif cmd == "listfiles":
            self.list_files()
        elif cmd == "startprocess" and args:
            self.start_process(args[0])
        elif cmd == "stopprocess" and args:
            self.stop_process(args[0])
        elif cmd == "listprocesses":
            self.list_processes()
        elif cmd == "adduser" and len(args) == 2:
            self.add_user(args[0], args[1])
        elif cmd == "logout":
            self.logout()
        elif cmd == "exit":
            self.speak("Exiting Custom Operating System Simulation")
            print("Exiting CustomOS. Goodbye!")
            exit()
        else:
            print("Invalid command. Type 'help' for a list of commands.")
            self.speak("Invalid command")

    def run(self):
        self.welcome_message()
        self.authenticate()

        while True:
            command = input(f"{self.current_user}@CustomOS> ").strip()
            self.command_handler(command)

# Run the Custom OS Simulation
if __name__ == "__main__":
    os_simulation = CustomOS()
    os_simulation.run()
