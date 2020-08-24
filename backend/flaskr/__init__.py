import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        return response

    # GET categories endpoint
    @app.route("/api/categories")
    def get_categories():
        return jsonify({
            "success": True,
            "categories": get_categories_dict(),
        })

    # GET questions endpoint
    @app.route("/api/questions")
    def get_questions():
        page = int(request.args.get('page', '1'))
        questions = Question.query.all()
        start = QUESTIONS_PER_PAGE * (page-1)
        end = start + QUESTIONS_PER_PAGE

        total_questions = len(questions)
        if start >= total_questions:
            abort(404)

        return jsonify({
            "success": True,
            "questions": [question.format() for question in questions[start:end]],
            "total_questions": total_questions,
            "categories": get_categories_dict(),
            "current_category": None,
        })

    # DELETE question endpoint
    @app.route("/api/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                "success": True,
            }), 200
        except:
            return jsonify({
                "success": False,
            }), 422

    # POST question endpoint
    @app.route("/api/questions", methods=['POST'])
    def add_question():
        # validate data
        try:
            posted_data = request.get_json()
            if (len(posted_data['question']) == 0
                or len(posted_data['answer']) == 0
                or len(posted_data['category']) == 0
                    or int(posted_data['difficulty']) <= 0):
                raise ValueError('Invalid Data')
        except:
            return jsonify({
                "success": False,
            }), 400

        # insert question
        try:
            question = Question(posted_data['question'], posted_data['answer'],
                                posted_data['category'], int(posted_data['difficulty']))
            question.insert()
            return jsonify({
                "success": True,
                "question_id": question.id,
            }), 200
        except:
            return jsonify({
                "success": False,
            }), 422

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    ### Helper Methods ###
    '''
    # get categories dictionary
    def get_categories_dict():
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type
        return categories_dict

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    # handle not found error (404)
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    # handle internal server error (500)
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Server error has occured, please try again!'
        }), 500

    return app
