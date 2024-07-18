# FastAPI_MVC_SQLAlchemy

This project is a web application built with FastAPI, following the Model-View-Controller (MVC) design pattern, and using SQLAlchemy for database interactions.

## Features

- User registration and authentication
- CRUD operations for posts
- JWT-based authentication

## Models

The application uses two main models:

- `UserDB`: Represents a user in the database.
- `PostDB`: Represents a post in the database. Each post has an `id`, `text`, and `owner_id`. The `owner_id` is a foreign key that references the `id` of the user who owns the post.

## Running the Application

To run the application, you need to have Python installed on your machine. Then, you can install the required dependencies with:

```bash
pip install -r requirements.txt