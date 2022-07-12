import sys
from flask import (
    Flask,
    request,
    abort,
    jsonify
)
from flask_cors import CORS
import random
from sqlalchemy.exc import DBAPIError

from models import setup_db, Question
from helpers import (
    create_question,
    search_question,
    paginate_questions,
    get_categories_helper
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Allow '*' for origins
    CORS(app)

    """
    Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    Endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        categories = get_categories_helper()

        return jsonify({
            'success': True,
            'categories': categories,
        })

    """
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint returns a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three
     pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        categories = get_categories_helper()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': categories,
            'total_questions': len(selection)
        })

    """
    Endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(selection)
            })

        except (DBAPIError, AttributeError):
            print(sys.exc_info())
            abort(422)

    """
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    POST endpoint to get questions based on a search term.
    It returns any questions for whom the search term
    is a substring of the question.
    """
    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        try:
            if search_term is not None:
                return search_question(search_term, request)

            return create_question(body, request)
        except (DBAPIError, AttributeError):
            print(sys.exc_info())
            abort(500)

    """
    Endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        selection = Question.query.order_by(Question.id).filter(
            Question.category == category_id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': category_id
        })

    """
    POST endpoint to get questions to play the quiz.
    This endpoint takes category and previous question parameters
    and returns a random question within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_the_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        query = Question.query
        if quiz_category['type'] != 'click':
            query = query.filter(
                Question.category == int(quiz_category['id']))

        questions = query.filter(
            Question.id.notin_(previous_questions)).all()

        question = None
        if len(questions) > 0:
            question = random.choice(questions).format()

        return jsonify({
            'success': True,
            'question': question
        })

    """
    Error handlers for all expected errors
    including 400, 404, 422, and 500.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {"success": False, "error": 400, "message": "bad request"}
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def server_error(error):
        return jsonify(
            {"success": False, "error": 500, "message": "server error"}
        ), 500

    return app
