import os
from tkinter.messagebox import QUESTION
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, select_questions):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in select_questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_category = {
            category.id: category.type for category in categories}
        return jsonify({
            "success": True,
            "categories": formatted_category,
            "total_category": len(formatted_category)
        })

    @app.route("/questions")
    def get_questions():
        select_questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, select_questions)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        formatted_category = {
            category.id: category.type for category in categories}

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(select_questions),
            "categories": formatted_category
        })

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                "success": True,
                "deleted": question_id,
                "total_questions": len(Question.query.all())
            })

        except BaseException:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def create_questions():
        data = request.get_json()

        new_question = data.get('question', None)
        new_answer = data.get('answer', None)
        new_category = data.get('category', None)
        difficulty = data.get('difficulty', None)

        searchTerm = data.get('searchTerm', None)

        try:
            if searchTerm:
                select_questions = Question.query.order_by(
                    Question.id).filter(
                    Question.question.ilike(f'%{searchTerm}%'))

                current_questions = paginate_questions(
                    request, select_questions)

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(select_questions.all())
                    }
                )

            else:

                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=difficulty)
                question.insert()

                select_questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(
                    request, select_questions)
                print(current_questions)
                return jsonify({
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all())
                })

        except BaseException:
            abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def question_category(category_id):
        categories = Category.query.filter(
            Category.id == category_id).one_or_none()

        if categories is None:
            abort(404)

        try:
            select_questions = Question.query.filter(
                Question.category == category_id).all()
            current_questions = paginate_questions(request, select_questions)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(select_questions)
            })

        except BaseException:
            abort(400)

    @app.route("/quizzes", methods=["POST"])
    def random_quizzes():

        data = request.get_json()

        quiz_category = data.get("quiz_category", None)
        previous_questions = data.get("previous_questions", None)

        try:
            if quiz_category['id'] == 0:
                question_list = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                question_list = Question.query.filter(
                    Question.category == quiz_category['id']).filter(
                    Question.id.notin_(previous_questions)).all()

            formatted_question = [question.format()
                                  for question in question_list]
            randomIndex = random.randint(0, len(formatted_question) - 1)
            # print(randomIndex)
            nextQuestion = formatted_question[randomIndex]
            return jsonify({
                "success": True,
                "question": nextQuestion
            })
        except BaseException:
            abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({"success": False, "error": 404,
                         "message": "resource not found"}), 404, )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify({"success": False, "error": 405,
                         "message": "method not allowed"}), 405, )

    @app.errorhandler(400)
    def bad_request(error):
        return(
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400
        )
    return app
