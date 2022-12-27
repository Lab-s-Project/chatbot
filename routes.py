from flask import (Flask, request, render_template, redirect, flash, url_for,
                   session, jsonify)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError

from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

from passlib.hash import sha256_crypt

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app, db, login_manager, bcrypt
from models import *
from forms import login_form, register_form
from chatbot import get_response


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=3)


def close_session(session):
    session.close()
    print("Session closed")


@app.route("/", strict_slashes=False)
@app.route("/home", methods=("GET", "POST"), strict_slashes=False)
def home():
    try:
        if not current_user.is_authenticated:
            flash('로그인 해주세요.', 'danger')
            return redirect(url_for('login'))
        else:
            return render_template("home.html")

    except Exception as e:
        print("Error : ", e)
    finally:
        close_session(db.session)
        pass


@login_required
@app.route("/profile", methods=['GET', 'POST'])
def profile():
    try:
        if not current_user.is_authenticated:
            flash('로그인 해주세요.', 'danger')
            return redirect(url_for('login'))
        else:
            try:
                user_id = current_user.get_id()
                user = User.query.filter_by(id=user_id).first_or_404()

                return render_template("profile.html", user=user)
            except Exception as e:
                flash(e, "danger")
            
            finally:
                close_session(db.session)

    except Exception as e:
        print(e)
    finally:
        close_session(db.session)
        pass


@app.post("/predict")
def predict():
    user_id = current_user.get_id()
    text = request.get_json().get('message')

    # add message to the database
    storeMessage(user_id, "message", text)
    response = get_response(text)

    # add response to the database
    storeResponse(user_id, "response", response)

    # return response to UI
    answer = {"answer": response}
    return jsonify(answer)


def storeMessage(id, _type, text):
    user_id = id
    type = _type
    text = text

    chat = Chat(user_id=user_id, type=type, text=text)
    db.session.add(chat)
    db.session.commit()
    
    close_session(db.session)
    
    return None


def storeResponse(id, _type, text):
    user_id = id
    type = _type
    text = text

    chat = Chat(user_id=user_id, type=type, text=text)
    db.session.add(chat)
    db.session.commit()
    
    close_session(db.session)
    return None


@login_required
@app.get("/history")
def get_history():
    try:
        if not current_user.is_authenticated:
            flash('로그인 해주세요.', 'danger')
            return redirect(url_for('login'))
        else:
            try:
                user_id = current_user.get_id()
                history_filters = Chat.query.filter_by(
                    user_id=user_id).order_by(Chat.created_at.asc()).all()

                convo = []
                for his in history_filters:
                    type = his.type
                    text = his.text
                    created_at = his.created_at

                    history = {
                        "type": type,
                        "text": text,
                        "created_at": created_at
                    }
                    convo.append(history)

                return jsonify(convo)
            except InvalidRequestError:
                db.session.rollback()
                flash("시스템 오류입니다. 나중에 다시 시도해 주세요.", "danger")
            except IntegrityError:
                db.session.rollback()
                flash("사용자가 이미 존재 합니다", "warning")
            except DataError:
                db.session.rollback()
                flash("잘못된 항목", "warning")
            except InterfaceError:
                db.session.rollback()
                flash("Error connecting to the database", "danger")
            except DatabaseError:
                db.session.rollback()
                flash("Error connecting to the database", "danger")
            except BuildError:
                db.session.rollback()
                flash("An error occurred!", "danger")
            
            finally:
                close_session(db.session)
                pass

    except Exception as e:
        print('Error! Code: {c}, Message, {m}'.format(c=type(e).__name__,
                                                      m=str(e)))
    finally:
        pass


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    try:
        if not current_user.is_authenticated:
            form = login_form()

            if form.validate_on_submit():
                try:
                    user = User.query.filter_by(
                        student_id=form.student_id.data).first()
                    if sha256_crypt.verify(form.password.data, user.password):
                        login_user(user)
                        return redirect(url_for('home'))
                    else:
                        flash("잘못된 아이디 또는 비밀번호입니다.", "danger")
                except Exception as e:
                    flash(e, "danger")
                
                finally:
                    close_session(db.session)

            return render_template("auth.html",
                                   form=form,
                                   title="로그인",
                                   btn_action="로그인",
                                   head_title="로그인 하기",
                                   head_text="아이디/비밀번호를 넣어주세요.")
        return redirect(url_for('home'))
    except Exception as e:
        print('Error! Code: {c}, Message, {m}'.format(c=type(e).__name__,
                                                      m=str(e)))
    finally:
        close_session(db.session)
        pass


# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            student_id = form.student_id.data
            name = form.name.data
            phone_number = form.phone_number.data
            school_name = form.school_name.data
            grade = form.grade.data
            class_no = form.class_no.data
            password = form.password.data

            newuser = User(
                student_id=student_id,
                type="Student",
                name=name,
                school_name=school_name,
                phone_number=phone_number,
                grade=grade.lstrip("0"),
                class_no=class_no.lstrip("0"),
                password=sha256_crypt.hash(password),
            )

            db.session.add(newuser)
            db.session.commit()
            flash("계정을 만들었습니다. 로그인 해주세요.", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash("시스템 오류입니다. 나중에 다시 시도해 주세요.", "danger")
        except IntegrityError:
            db.session.rollback()
            flash("사용자가 이미 존재 합니다", "warning")
        except DataError:
            db.session.rollback()
            flash("잘못된 항목", "warning")
        except InterfaceError:
            db.session.rollback()
            flash("Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash("Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash("An error occurred !", "danger")
        
        finally:
            close_session(db.session)
            pass
        
    return render_template("auth.html",
                           form=form,
                           title="생성하기",
                           btn_action="생성하기",
                           head_title="처음이신가요",
                           head_text="챗봇을 사용하기 위한 계정을 만들어주세요.")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_found(e):
    return render_template("405.html"), 405


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
