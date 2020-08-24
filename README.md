# Trivia

Udacity Advanced Track Full Stack API Final Project

## Installation
### Backend
```bash
pip install -r requirements.txt
```

### Frontend
```bash
npm install
```

## Run
### Backend
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
### Frontend
```bash
npm start
```

## API Endpoints
### GET /api/categories
- Response body:
  ```bash
  {
    "categories": {
      "{id}": "{type}",
      ...
    }, 
    "success": true
  }
  ```

### GET /api/questions
- Request args: ```?page={page_number}```
- Response body:
  ```bash
  {
    "categories": {
      "{id}": "{type}",
      ...
    }, 
    "current_category": null, 
    "questions": [
      {
        "id": {question_id}, 
        "question": "{question_question}",
        "answer": "{question_answer}", 
        "category": {question_category}, 
        "difficulty": {question_difficulty}
      },
      ...
    ], 
    "success": true, 
    "total_questions": {total_questions_number}
  }
  ```

### DELETE /api/questions/<int:question_id>
- Response body:
  ```bash
  {
    "success": true
  }
  ```

### POST /api/questions
- can be used to add new question or search questions
- Add new question:
    - Request body:
      ```bash
      {
        "question": "{question}",
        "answer": "{title}",
        "difficulty": {difficulty},
        "category": {category}
      }
      ```
      - Response body:
      ```bash
      {
        "question_id": 59, 
        "success": true
      }
      ```
- Search questions:
  - Request Body:
    ```bash
    {
      "search_term": "{search_term}"
    }
    ```
    - Response body:
    ```bash
    {
      "current_category": {category_id|null}, 
      "questions": [
        {
          "id": {question_id}, 
          "question": "{question_question}",
          "answer": "{question_answer}", 
          "category": {question_category}, 
          "difficulty": {question_difficulty}
        },
        ...
      ],
      "total_questions": {total_questions_number},
      "success": true
    }
    ```

### GET /api/categories/<int:category_id>/questions
- Response body:
  ```bash
  {
    "current_category": {
      "id": {category_id},
      "type": {category_type},
    }, 
    "questions": [
      {
        "id": {question_id}, 
        "question": "{question_question}",
        "answer": "{question_answer}", 
        "category": {question_category}, 
        "difficulty": {question_difficulty}
      },
      ...
    ], 
    "success": true, 
    "total_questions": {total_questions_number}
  }
  ```

### POST /api/quizzes
- Request body:
  ```bash
  {
      "previous_questions": [],
      "quiz_category": {
          "type": "{category_type}",
          "id": {category_id}
      }
  }
  ```
- Response body:
  ```bash
  {
    "question": {
      "id": {question_id}, 
      "question": "{question_question}",
      "answer": "{question_answer}", 
      "category": {question_category}, 
      "difficulty": {question_difficulty}
    },
    "success": true
  }
  ```

### Errors Response Format
```bash
{
  "success": {boolean},
  "error": {status_code},
  "message": "{status_message}"
}
```