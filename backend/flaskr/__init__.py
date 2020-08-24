from flask import Flask, request, abort, jsonify
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
        }), 200

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
        }), 200

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
        # determine request
        try:
            posted_data = request.get_json()
            if 'question' in posted_data:
                return handle_add_question(posted_data)
            elif 'search_term' in posted_data:
                return handle_search_question(posted_data)
            else:
                raise ValueError('Invalid Request')
        except:
            return jsonify({
                "success": False,
            }), 400

    def handle_add_question(posted_data):
        # validate data
        try:
            if (len(posted_data['question']) == 0
                or len(posted_data['answer']) == 0
                or len(str(posted_data['category'])) == 0
                    or int(posted_data['difficulty']) <= 0):
                raise ValueError('Invalid Data')
        except:
            return jsonify({
                "success": False,
            }), 400
        # insert question
        try:
            question = Question(posted_data['question'], posted_data['answer'],
                                str(posted_data['category']), int(posted_data['difficulty']))
            question.insert()
            return jsonify({
                "success": True,
                "question_id": question.id,
            }), 200
        except:
            return jsonify({
                "success": False,
            }), 422

    def handle_search_question(posted_data):
        # search question
        try:
            questions = Question.query.filter(Question.question.ilike(
                '%' + posted_data['search_term'] + '%')).all()
            return jsonify({
                "success": True,
                "questions": [question.format() for question in questions],
                "total_questions": len(questions),
                "current_category": None,
            })
        except:
            return jsonify({
                "success": False,
            }), 422

    # GET category questions endpoint
    @app.route("/api/categories/<int:category_id>/questions")
    def get_category_questions(category_id):
        questions = Question.query.filter(
            Question.category == str(category_id)).all()

        category = Category.query.get(category_id)

        return jsonify({
            "success": True,
            "questions": [question.format() for question in questions],
            "total_questions": len(questions),
            "current_category": category.format(),
        }), 200

    # POST quizzes endpoint
    @app.route("/api/quizzes", methods=['POST'])
    def get_quiz_question():
        posted_data = request.get_json()
        quiz_category = str(posted_data['quiz_category']['id'])
        previous_questions = posted_data['previous_questions']

        # get all questions of a specific category
        if quiz_category == '0':
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == quiz_category).all()

        # check if all questions are previously included
        if len(questions) == len(previous_questions):
            question = False
        else:
            while True:
                question_index = random.randrange(len(questions))
                question = questions[question_index]
                if question.id not in previous_questions:
                    break

        return jsonify({
            "success": True,
            "question": question.format() if question else False,
        })

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

    # handle not found error (404)
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    # handle unprocessable entity error (422)
    @app.errorhandler(422)
    def unprocessable_entity_error(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    # handle internal server error (500)
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Server error has occured, please try again!'
        }), 500

    return app
