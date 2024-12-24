# Event Manager Client App

## Overview

The Event Manager Client App is a Streamlit-based web application that allows users to manage events using a dynamic, user-friendly interface. The app is integrated with AWS services such as Cognito for authentication and API Gateway with Lambda functions for backend operations. Users can create, update, delete, and view events through a clean and intuitive interface.

## Features

- **User Authentication**: Secure login via AWS Cognito.
- **Event Management**: Add, modify, delete, and view events.
- **Dynamic Filtering**: Filter events by categories such as All Events, Upcoming Events, and Past Events.
- **Interactive UI**: Select events through flashcards, with highlighted selection.
- **API Integration**: Communication with a DynamoDB backend via API Gateway.

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: AWS Lambda
- **Database**: AWS DynamoDB
- **Authentication**: AWS Cognito
- **API Management**: AWS API Gateway

## Project Structure
```
project/
│
├── app.py             # Main entry point for the Streamlit application
├── config.py          # Configuration variables (Cognito, API details)
├── auth.py            # Authentication-related functions
├── api.py             # API interaction functions
├── ui_components.py   # Functions for UI components (sidebar, flashcards, etc.)
├── utils.py           # Utility functions
├── static/            # Static assets such as the logo
└── README.md          # Documentation
```

## Setup and Installation

### Prerequisites

- Python 3.8 or later
- AWS account with Cognito, API Gateway, and DynamoDB configured
- Required Python packages (listed in `requirements.txt`)

### Steps

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd project
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure AWS services in `config.py`:
    ```python
    COGNITO_DOMAIN = "<Your Cognito Domain>"
    CLIENT_ID = "<Your Client ID>"
    CLIENT_SECRET = "<Your Client Secret>"
    REDIRECT_URI = "http://localhost:8501/"
    TOKEN_ENDPOINT = f"{COGNITO_DOMAIN}/oauth2/token"
    API_BASE_URL = "<Your API Gateway Base URL>"
    ```

4. Run the application:
    ```sh
    streamlit run app.py
    ```

5. Open the app in your browser at `http://localhost:8501`.

## Usage

### Authentication

- On launching the app, you will be redirected to the AWS Cognito login page.
- Sign in or register to access the application.

### Managing Events

#### Create Event:

- Use the form in the sidebar to enter event details and click "Submit".

#### Modify Event:

- Select an event by clicking "Select" on its flashcard.
- Click "Modify Selected" in the navigation bar to edit its details.

#### Delete Event:

- Select an event by clicking "Select" on its flashcard.
- Click "Delete Selected" in the navigation bar to remove it.

#### Filter Events:

- Use the filter navigation bar at the top to switch between All Events, Upcoming Events, and Past Events.

## Key Components

- **Sidebar**: Event creation and modification form.
- **Navigation Bar**: Event filters and action buttons (Modify/Delete Selected).
- **Flashcards**: Visual representation of events with selection capability.

## API Integration

The app communicates with AWS API Gateway to perform CRUD operations:

- **POST**: Create a new event.
- **PUT**: Update an existing event.
- **DELETE**: Remove an event by ID.
- **GET**: Retrieve events from DynamoDB.

## Contributing

1. Fork the repository.
2. Create a new feature branch:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. Commit your changes:
    ```sh
    git commit -m "Add your message"
    ```
4. Push to the branch:
    ```sh
    git push origin feature/your-feature-name
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or support, please contact:

- **Email**: adrisanpu@gmail.com
- **GitHub Issues**: Open an Issue