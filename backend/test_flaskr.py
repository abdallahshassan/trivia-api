import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        response = self.client().get('/api/categories')
        data = json.loads(response.data)
        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        response = self.client().get('/api/questions?page=1')
        data = json.loads(response.data)
        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])

    def test_get_questions_404(self):
        response = self.client().get('/api/questions?page=100')
        # assertions
        self.assertEqual(response.status_code, 404)

    def test_delete_question(self):
        # create question for deletion
        question = Question(
            question='Test question for deletion',
            answer='Answer of test question for deletion',
            difficulty=1,
            category='1')
        question.insert()
        response = self.client().delete('/api/questions/' + str(question.id))
        # assertions
        self.assertEqual(response.status_code, 200)

    def test_delete_question_422(self):
        response = self.client().delete('/api/questions/10000')
        # assertions
        self.assertEqual(response.status_code, 422)

    def test_insert_question(self):
        insert_data = {
            "question": "Test question for insertion",
            "answer": "Answer of test question for insertion",
            "difficulty": 1,
            "category": "1",
        }
        response = self.client().post('/api/questions', json=insert_data)
        data = json.loads(response.data)
        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_id'])
        # delete that question
        question = Question.query.get(data['question_id'])
        question.delete()

    def test_insert_question_400(self):
        insert_data = {
            "question": "Test question for insertion",
            "answer": "Answer of test question for insertion",
        }
        response = self.client().post('/api/questions', json=insert_data)
        data = json.loads(response.data)
        # assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
