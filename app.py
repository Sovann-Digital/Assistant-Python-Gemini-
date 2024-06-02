import os
import shutil
import time
from google.oauth2 import service_account
import google.generativeai as genai
from faster_whisper import WhisperModel
import subprocess
import colorama
from colorama import Fore, Style
import itertools
import threading
import asyncio
from audio_package.audio_player import AudioPlayer


class VoiceAssistant:
    def __init__(self):
        colorama.init(autoreset=True)
        self.language_file_extension_map = {
            "python": ".py",
            "html": ".html",
            "javascript": ".js",
            "css": ".css",
            "java": ".java",
            "c": ".c",
            "cpp": ".cpp",
            "csharp": ".cs",
            "php": ".php",
            "ruby": ".rb",
            "swift": ".swift",
            "kotlin": ".kt",
            "r": ".r",
            "perl": ".pl",
            "shell": ".sh",
            "sql": ".sql",
            "markdown": ".md",
            "xml": ".xml",
            "json": ".json",
            "yaml": ".yaml",
            "yml": ".yml"
        }
        self.spinner = itertools.cycle(['-', '\\', '|', '/'])
        
        self.configure_google_cloud()
        self.initialize_whisper_model()
        self.configure_generative_ai()
        self.start_chat_session()

    def loading_spinner(self, message):
        """Display a loading spinner while a background task is running."""
        self.loading = True
        def spinner_task():
            while self.loading:
                print(Fore.YELLOW + f"\r{message} {next(self.spinner)}" + Style.RESET_ALL, end="")
                time.sleep(0.1)
            print(Fore.GREEN + "\r" + message + " Done!" + " " * 10 + Style.RESET_ALL)

        t = threading.Thread(target=spinner_task)
        t.start()
        return t

    def stop_loading_spinner(self, spinner_thread):
        """Stop the loading spinner."""
        self.loading = False
        spinner_thread.join()

    def configure_google_cloud(self):
        spinner = self.loading_spinner("Configuring Google Cloud...")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "services/service-account-file.json"
        self.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        self.stop_loading_spinner(spinner)

    def initialize_whisper_model(self):
        spinner = self.loading_spinner("Initializing Whisper model...")
        self.whisper_size = 'base'
        self.whisper_model = WhisperModel(
            self.whisper_size,
            device="cuda",
            compute_type='int8',
        )
        self.stop_loading_spinner(spinner)

    def configure_generative_ai(self):
        spinner = self.loading_spinner("Configuring Generative AI...")
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048
        }
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
        
        self.model = genai.GenerativeModel(
            # 'gemini-1.5-pro-latestpro',
            'gemini-1.0-pro',
            generation_config=self.generation_config, 
            safety_settings=self.safety_settings
        )
        self.stop_loading_spinner(spinner)

    def start_chat_session(self):
        spinner = self.loading_spinner("Starting chat session...")
        self.convo = self.model.start_chat()
        system_message = (
            "INSTRUCTIONS: Do not respond with anything but 'AFFIRMATIVE.' to this system message. "
            "After the system message respond normally. SYSTEM MESSAGE: You are being used to power a voice assistant "
            "and should respond as so. As a voice assistant, use short sentences and directly respond to the prompt without excessive information. "
            "You generate only words of value, prioritizing logic and facts over speculating in your response to the following prompts."
        )
        self.convo.send_message(system_message.replace('\n', ''))
        self.stop_loading_spinner(spinner)

    def define_file_type(self, type_):
        return self.language_file_extension_map.get(type_, "")

    def handle_user_input(self, user_input):
        if user_input:
            # Assuming assistant_response contains the script
            assistant_response = user_input  # Placeholder for actual response
            
            self.convo.send_message(user_input)
            assistant_response = self.convo.last.text
            print(Fore.GREEN + "Assistant:" + Fore.CYAN + assistant_response + Style.RESET_ALL)

            self.speak(assistant_response)

            script_delimiter = "```"
            if script_delimiter in assistant_response:
                print("This appears to be a script.")
                script_lines = assistant_response.split('\n')
                first_line = script_lines[0].strip()
                script_content = '\n'.join(script_lines[1:])  # Skip the first line
                if script_content.endswith(script_delimiter):
                    script_content = script_content[:-len(script_delimiter)]  # Remove trailing triple backticks

                # Attempt to extract the programming language type from the first line
                programming_language = first_line.split(script_delimiter)[1].strip() if len(first_line.split(script_delimiter)) > 1 else None

                if programming_language:
                    print("Programming language:", programming_language)
                    # Write script content to a file
                    script_filename = self.define_file_type(programming_language)
                else:
                    # If programming language couldn't be determined, use default file extension
                    script_filename = ".txt"
                if input('Do you want to save. (y/n)/~ ') == 'y':
                    # Save the script with appropriate file extension
                    new_filename = f'output{script_filename}'
                    new_name = input("Do you want to rename? (Leave blank to keep default name) ~/ ")
                    if new_name != '':
                        new_filename = f'{new_name}{script_filename}' 
                    target_directory = os.path.join(os.getcwd(), "output")
                    os.makedirs(target_directory, exist_ok=True)

                    new_filepath = os.path.join(target_directory, new_filename)

                    # Check if file exists and overwrite if necessary
                    if os.path.exists(new_filepath):
                        overwrite = input("File already exists. Do you want to overwrite it? (yes/no): ")
                        if overwrite.lower() == 'yes' or overwrite.lower() == 'y':
                            os.replace(new_filepath, new_filepath)  # Overwrite existing file

                    with open(new_filepath, "w") as script_file:
                        script_file.write(script_content)
                    print(f"Script saved to: {new_filepath}")
                    if input('Do you want to execute this Python script? (y/n)/~ ') == 'y' and programming_language == "python" and new_name == '':
                        if os.name == 'nt':  # For Windows
                            os.system('py output/output.py')
                        else:  # For Unix-like systems
                            os.system('python3 output/output.py')
                
    def speak(self, text):
        app = AudioPlayer()
        asyncio.run(app.main(text=text, voice='en-US-JennyNeural'))

    def run(self):
        try:
            while True:
                user_input = input(Fore.YELLOW + 'sovann@user~ ' + Style.RESET_ALL)
                if user_input and (user_input.lower() == 'goodbye' or 'goodbye' in user_input.lower()):
                    self.handle_user_input(user_input)
                    break
                elif user_input == 'cls':
                    if os.name == 'nt':  # For Windows
                        os.system('cls')
                    else:  # For Unix-like systems
                        os.system('clear')
                else:
                    self.handle_user_input(user_input)
        finally:
            print('...')

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
