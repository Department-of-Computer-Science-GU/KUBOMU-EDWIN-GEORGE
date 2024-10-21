# Chat Application

## Overview

This is a Django-based chat application designed for secure and real-time messaging. The app allows users to send and receive messages securely using encryption.

## Features

- User authentication (login and registration)
- Secure message encryption and decryption
- Real-time messaging using Django Channels
- User-friendly interface

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Department-of-Computer-Science-GU/KUBOMU-EDWIN-GEORGE.git

2. Navigate to the project directory:
     ```bash

          cd ChatApp


3. Create a virtual environment:
   	  ```bash
   

         python -m venv venv


4. Activate the virtual environment:
        ```bash

       # For Windows
        venv\Scripts\activate

       # For macOS/Linux
        source venv/bin/activate

5. Install the required packages:
   		  ```bash

        pip install -r requirements.txt


6. Run database migrations:
       ```bash

        python manage.py migrate

7. Collect static files (as they are not uploaded):
       ```bash

       python manage.py collectstatic

You will be prompted to confirm the action. Type yes to proceed.

8. Start the development server:
    ```bash
      python manage.py runserver


9. Open your browser and go to http://127.0.0.1:8000/.

Usage

	•	Users can register and log in to access the chat interface.
	•	Messages are encrypted for security.
	•	The application is designed for real-time messaging.

Note

This project is currently in progress. Some features are still missing, including:

	•	Group chat functionality
	•	User profile management
	•	Message history
	•	Additional security measures

Feel free to contribute by forking the repository and submitting a pull request.



This template provides clear instructions for users to set up the project, including creating a virtual environment and collecting static files, ensuring they have everything needed to run the application.
