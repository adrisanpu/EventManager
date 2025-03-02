# Event Manager Client App

## Overview

The Event Manager Client App is a Streamlit-based web application that allows users to manage events using a dynamic, user-friendly interface. The app is integrated with AWS services such as Cognito for authentication and API Gateway with Lambda functions for backend operations. Users can create, update, delete, and view events through a clean and intuitive interface.

![image](https://github.com/user-attachments/assets/9568a295-8460-4327-8a36-e797de27fc68)

## Features

- **User Authentication**: Secure login via AWS Cognito.
- **Event Management**: Add, modify, delete, and view events.
- **Dynamic Filtering**: Filter events by categories such as All Events, Upcoming Events, and Past Events.
- **Interactive UI**: Select events through flashcards, with highlighted selection.
- **API Integration**: Communication with a DynamoDB backend via API Gateway.

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: AWS Lambda
- **Database**: AWS DynamoDB and AWS S3
- **Authentication**: AWS Cognito
- **API Management**: AWS API Gateway
  
![eventapi_aws drawio](https://github.com/user-attachments/assets/28baadc8-428e-4aad-ba19-82d3cb30904b)

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

3. Configure AWS services in a folder `.streamlit/secrets.toml`:
    ```text
    [default]
    COGNITO_DOMAIN = [COMPLETE]
    CLIENT_ID = [COMPLETE]
    CLIENT_SECRET = [COMPLETE]
    REDIRECT_URI = [COMPLETE]
    API_BASE_URL = [COMPLETE]
    
    [s3]
    S3_BUCKET_NAME = [COMPLETE]
    S3_REGION = [COMPLETE]
    
    [aws]
    AWS_ACCESS_KEY = [COMPLETE]
    AWS_SECRET_KEY = [COMPLETE]
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


## Contact

For questions or support, please contact:

- **Email**: adrisanpu@gmail.com
- **GitHub Issues**: Open an Issue
