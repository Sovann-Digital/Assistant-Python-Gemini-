# Voice Assistant

This Voice Assistant uses Google's Generative AI and Whisper models to provide assistance with various tasks such as code generation, file handling, and executing commands. 

## Prerequisites

1. **Service Account File**: Ensure you have your `service-account-file.json` from Google Cloud.
2. **API Key**: Obtain your Google API key.

## Getting the Service Account File

1. **Go to the Google Cloud Console**: Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2. **Select Your Project**: If you don't have a project, create a new one.
3. **Enable APIs**: Ensure the APIs you need are enabled, especially the Generative AI and any other required APIs.
4. **Create a Service Account**:
    - Go to the [Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts).
    - Click `Create Service Account`.
    - Fill in the required details and click `Create`.
5. **Create and Download a Key**:
    - Click on the created service account.
    - Go to the `Keys` tab.
    - Click `Add Key` > `Create New Key`.
    - Choose `JSON` and click `Create`. The file will be downloaded automatically.
6. **Move the Service Account File**: Move the downloaded `service-account-file.json` to the `services` folder in your project.

## Setup

1. **Move Service Account File**: Move your `service-account-file.json` to the `services` folder.
2. **Create Environment File**: Create a `.env` file in the root directory of your project and add your Google API key:
    ```
    GOOGLE_API_KEY = "<YOUR_API_KEY>"
    ```
3. **Install Requirements**: Open your terminal and run the following command to install the necessary packages:
    ```
    python -m pip install -r requirements.txt
    ```
    or
    ```
    py -m pip install -r requirements.txt
    ```

4. **Configure Whisper Model**: If you are using a CPU, change the `device` parameter in the `initialize_whisper_model` method to `cpu`. If you are using CUDA, change it to `cuda`:

    - **CPU Configuration**:
        ```python
        def initialize_whisper_model(self):
            spinner = self.loading_spinner("Initializing Whisper model...")
            self.whisper_size = 'base'
            self.whisper_model = WhisperModel(
                self.whisper_size,
                device="cpu",
                compute_type='int8',
            )
            self.stop_loading_spinner(spinner)
        ```
    - **CUDA Configuration**:
        ```python
        def initialize_whisper_model(self):
            spinner = self.loading_spinner("Initializing Whisper model...")
            self.whisper_size = 'base'
            self.whisper_model = WhisperModel(
                self.whisper_size,
                device="cuda",
                compute_type='int8',
            )
            self.stop_loading_spinner(spinner)
        ```

## Usage

1. Run the voice assistant script:
    ```
    python app.py
    ```

2. Interact with the assistant using the console prompts.

## Notes

- Use the assistant responsibly. This tool is intended for good purposes, such as serving as a copilot in your development activities.

## Warnings

- **Warning**: Please use this AI responsibly and for good purposes only. This will help you in your copilot and more.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

