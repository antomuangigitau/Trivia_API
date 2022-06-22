# Trivia API Documentation

## Introduction

This API performs CRUD operations on the questions table in the Trivia database ie Create, Read, Update and Delete the questions

# Getting Started

## **Pre-requisites and Local Development**

Developers that want to use this project should have python, pip and Node installed on their local machines.

### Backend

From the backend folder run `pip install -r requirements.txt.` All required packages are included in the requirements file.
To run the application, run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flak run --reload
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder.
The application is run on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) by default and is a proxy in the frontend configuration.

### Frontend

From the frontend folder, run the following commands to start the client:

```
npm install // only once to install the dependencies
npm start
```

By default the frontend will run on **localhost:3000**

# API Reference

### Getting started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return four error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable

### Endpoints

#### `GET "/categories"`

- General:
  - Returns a dictionary of categories in which the key is of id and the values are the corresponding string of category, success value, and total categories
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_category": 6
}
```

#### `GET "/questions"`

- General:
  - Returns a paginated set of questions, all categories, total_questions and success value.
- Sample `curl http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```

#### `DELETE "/questions/{question_id}"`

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question and success value
- `curl -X DELETE http://127.0.0.1:5000/questions/31`

```json
{
  "deleted": 31,
  "success": true,
  "total_questions": 22
}
```

#### `POST "/questions"`

- General:

  - Sends a post request in order to add a new question

- Sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is going to apply for a Full Stack Job", "answer":"Me", "difficulty":"1", "category": "5"}'`

```
{
    "created": 32,
    "questions": [
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
    ],
    "success": true,
    "total_questions": 23
}
```

#### `POST "/questions"`

- General:
  - Sends a post request in order to search for a specific question by search term
- Sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "trees"}'`

- Returns: any array of questions, a number of totalQuestions that met the search term. and success value

```json
{
  "questions": [
    {
      "answer": "Canada",
      "category": 5,
      "difficulty": 2,
      "id": 24,
      "question": "Which country is the largest exporter of christmas trees?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### `GET "/categories/{category_id}/questions"`

- General:

  - Fetches questions for a category specified by id request argument

- Sample `curl http://127.0.0.1:5000/categories/1/questions`
- Returns: An object with questions for the specified category, total questions, and success value.

```json
{
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### `POST "/quizzes"`

- General:

  - Sends a post request in order to get the next question
  - Request Body:

    ```json
    {
      "previous_questions": [1, 4, 12],
      "quiz_category": {
        "id": 0,
        "type": "science"
      }
    }
    ```

  - Returns: a single new question object

  ```json
  {
    "question": {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  }
  ```

## Deployment N/A

## Authors

`Antony Mwangi`

# Acknowledgements

The awesome team at Udacity.
