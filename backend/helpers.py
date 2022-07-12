from unicodedata import category
from flask import jsonify
from models import Question, Category

QUESTIONS_PER_PAGE = 10

"""
paginate_questions:
slice selection, list, to return a number of items, less than or equal to
number of items in request query 'num_per_page' or default QUESTIONS_PER_PAGE
"""


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    num_per_page = request.args.get(
        "num_per_page", QUESTIONS_PER_PAGE, type=int)
    start = (page - 1) * num_per_page
    end = start + num_per_page

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


"""
get_categories_helper helper to get categories.
"""


def get_categories_helper():
    categories = Category.query.order_by(Category.id).all()
    category_dict = {}
    for category in categories:
        category_dict[category.id] = category.type
    
    return category_dict


"""
search_question returns questions matching a search term.
"""


def search_question(search_term, request):
    selection = Question.query.order_by(Question.id).filter(
        Question.question.ilike(f"%{search_term}%")
    )
    current_questions = paginate_questions(request, selection)

    return jsonify(
        {
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection.all()),
        }
    )


"""
create_question creates a question and persists in database. Creates
category if it doesn't exist.
"""


def create_question(body, request):
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', 0)
    new_difficulty = body.get('difficulty', None)

    if new_category == 'other':
        category_to_create = body.get('newCategory', None).capitalize()
        category = Category.query.filter(
            Category.type == category_to_create).one_or_none()

        if category is None:
            category = Category(type=category_to_create)
            category.insert()
        new_category = category.id

    question = Question(
        question=new_question,
        answer=new_answer,
        difficulty=new_difficulty,
        category=int(new_category)
    )
    question.insert()

    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(selection)
    })
