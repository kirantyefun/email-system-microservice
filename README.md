
# Email Microservice System

This repository contains the source code for an email microservice system built with Django REST Framework, RabbitMQ, and Sendgrid API. It consists of three services that run in a Minikube cluster:

-   **EmailSystem Service** - a Django project that provides a REST API to create and send emails, as well as to retrieve sent email logs. It interacts with a Postgresql database running on the local machine.
-   **EmailSender Service** - a Python script that runs in a separate pod and listens to a RabbitMQ queue for email messages. When it receives a message, it sends an email using the Sendgrid API. It is designed to be horizontally scalable, meaning that multiple instances of the script can run in parallel to handle a high volume of emails.
-   **RabbitMQ** - an official Docker image that runs a message broker to handle communication between the EmailSystem Service and EmailSender Service.

## Getting Started

To run the email microservice system locally, you will need to install the following dependencies:

-   [Docker](https://www.docker.com/products/docker-desktop)
-   [Minikube](https://minikube.sigs.k8s.io/docs/start/)
-   [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

Once you have these dependencies installed, you can follow these steps:

1.  Clone this repository: `https://github.com/kirantyefun/email-system-microservice.git`
2.  Navigate to the `email-microservice` directory: `cd email-microservice`
3.  Start Minikube: `minikube start`
4.  Apply the Kubernetes manifests: `kubectl apply -f manifests/`
5.  Wait for the pods to start: `kubectl get pods`
6.  Port-forward the EmailSystem Service to your local machine: `kubectl port-forward service/emailsystem-service 8000:8000`
7.  Open your web browser and navigate to [http://localhost:8000](http://localhost:8000/)
8.  Use the API to create and send emails!

**Note**: You will need to create a Sendgrid API key for yourself. In case you don't have domain, you need to authorize sender email. Then, Use the same email to send emails for testing purposes.

## API Endpoints for Users


Base URL: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)

Authentication: Token-based authentication is used for accessing the API endpoints. Users can obtain an authentication token by sending a POST request to the `login/` endpoint with their credentials.

## User Endpoints:

1.  **POST api/v1/users/register/**
    
    Endpoint for user registration. Users can create a new account by providing their email, username and password.
    
    Request Body:
    
    
    `{
      "email": "example_user@example.com",
      "username": "example_user",
      "password": "password123"
    }` 
    
    Response Body:
    
    `{
      "email": "example_user@example.com",
      "username": "example_user"
    }` 
    
2.  **POST api/v1/users/login/**
    
    Endpoint for user login. Users can obtain an authentication token by providing their email and password.
    
    Request Body:
    
    
    `{
      "username": "example_user@example.com",
      "password": "password123"
    }` 
    
    Response Body:

    `{
      "email": "example_user@example.com",
      "token": "c31d75f182b1e016c0f3592a60a99b18faa36efc"
    }` 
    
3.  **POST api/v1/users/logout/**
    
    Endpoint for user logout. Users can log out by sending a POST request with their authentication token.
    
    Request Body:
    
    `{}` 
    
    Response Body:
    
    
    `{}` 
    
## EmailTemplate Endpoints:

1.  **POST api/v1/emails/email-template/**
    
    Endpoint for email template creation. Only admin Users can create a new email-template.
    
    Request Body:
    
    
    `{
	"name": "Sample Template 11",
	"subject": "Sample Subject 11",
	"body": "Sample Body 11"
}` 
    
    Response Body:
    
    `{
	"id": 5,
	"name": "Sample Template 11",
	"subject": "Sample Subject 11",
	"body": "Sample Body 11",
	"created": "2023-03-30T06:54:15.278178Z",
	"modified": "2023-03-30T06:54:15.278239Z"
}` 
    
2.  **GET api/v1/emails/email-template/**
    
    Endpoint to list existing email-templates. Any user(authenticated/unauthenticated) can view existing email templates.
    
    
    Response Body: 
    
    `
    "results": [
		{
			"id": 1,
			"name": "Welcome Onboard",
			"subject": "Welcome Onboard",
			"body": "We are please to offer you this role. Onboarding will begin from tomorrow.",
			"created": "2023-03-25T14:59:11.108300Z",
			"modified": "2023-03-25T14:59:11.114470Z"
		},
		{
			"id": 2,
			"name": "Sorry Template",
			"subject": "Better Luck Next Time",
			"body": "We appreciate your interest in this role but we are sorry to inform you that not moving forward with your application.",
			"created": "2023-03-25T14:59:11.108300Z",
			"modified": "2023-03-25T14:59:11.114470Z"
		},
    `

3. **Update, PartialUpdate and Retrieve also available as PUT, PATCH and GET respectively**
    
## SentEmail Endpoints:

1.  **POST api/v1/emails/sent-email/**
    
    Endpoint for sending email. Creates a single sent_email instance. Creates new instances of Recipient in bulk if not already present in DB. Associates sent_email instance with instances of Recipient. Sends email to the mentioned recipients using emailId of the user sending request.
    
    Request Body:
    
    `{
	"recipients": ["kirantyefun@gmail.com", "sayamiasis@gmail.com"],
	"template": 1
}` 
    
    Response Body:
    
    `{
	"message": "Email sent. It might take a while to deliver."
}` 
    
2.  **GET api/v1/emails/sent-email/**
    
    Endpoint to list all sent emails by current user. Only authenticated user can view their sent emails.
    
    - Accepted query params:
    
    | Param | Type | Detail|
    |--|--|--|
    | recipient1 | string |	EmailId of the recipient1 |
    | recipient2 | string |	EmailId of the recipient2 |
    | recipientN | string |	EmailId of the recipientN |
    | start_time | datetime | start datetime of the range of timeframe|
    | end_time | datetime | end datetime of the range of timeframe|
    
    Example request with query params:
    - *localhost:8000/api/v1/emails/sent-email/?recipient=1@gmail.com&recipient=3@gmail.com&start_time=2023-03-25*
    


## Development

If you want to contribute to this project or run it in a development environment, you can follow these steps:

1.  Clone this repository: `https://github.com/kirantyefun/email-system-microservice.git`
2.  Navigate to the `email-microservice` directory: `cd email-microservice`
3.  Create a virtual environment: `python3 -m venv venv` or any other virtual environment of your choice
4.  Activate the virtual environment: `source venv/bin/activate`
5.  Install the dependencies: `pip install -r requirements.txt`
6.  Set up the database: `python manage.py migrate`
7.  Run the development server: `python manage.py runserver`
8.  Open your web browser and navigate to [http://localhost:8000](http://localhost:8000/)
9.  Use the API to create and send emails!


## Architecture

The email microservice system is designed to be a scalable and resilient system that can handle a high volume of emails. It is built using the following technologies and patterns:

-   **Django REST Framework** - provides a robust and flexible framework for building RESTful APIs in Python. It is deployed as service. So can be horizontally scaled.
-   **RabbitMQ** - a message broker that enables asynchronous. It is deployed as service. So can be horizontally scaled.
-   **Sender Service** - python script that waits to consume from a RabbitMQ queue, and sends emails using SendGrid API
