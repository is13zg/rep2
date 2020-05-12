from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.test import Tests
from data.tasks import Tasks
from data.answers import Answers
from data.form import RegisterForm, LoginForm, TestsForm, TasksForm, AnserForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

db_session.global_init("db/school.sqlite")
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
COUNT_OF_OTHER_QUESTIONS = 0
questions = []


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
@app.route("/school")
def index():
    session = db_session.create_session()
    test = session.query(Tests)
    return render_template("school.html", test=test)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация', form=form, message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.clas = form.clas.data
        user.occupation = form.occupation.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/school")
        return render_template('log_in.html', message="Неправильный логин или пароль", form=form)
    return render_template('log_in.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/school")


@app.route('/test', methods=['GET', 'POST'])
@login_required
def add_tests():
    global COUNT_OF_OTHER_QUESTIONS, questions
    form = TestsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        tests = Tests()
        tests.title = form.title.data
        tests.subject = form.subject.data
        tests.count_of_questions = form.count_of_questions.data
        tests.user_id = form.user_id.data
        session.merge(current_user)
        current_user.tests.append(tests)
        session.merge(current_user)
        session.commit()
        COUNT_OF_OTHER_QUESTIONS = int(form.count_of_questions.data)
        questions.append(COUNT_OF_OTHER_QUESTIONS)
        return redirect('/task')
    return render_template('tests.html', title='Добавление теста', form=form)


@app.route('/task', methods=['GET', 'POST'])
@login_required
def add_tasks():
    global COUNT_OF_OTHER_QUESTIONS
    form = TasksForm()
    if form.validate_on_submit():
        ses = db_session.create_session()
        test = ses.query(Tests).all()
        num = test[-1].id
        session = db_session.create_session()
        tasks = Tasks()
        tasks.title = form.title.data
        tasks.ans1 = form.ans1.data
        tasks.ans2 = form.ans2.data
        tasks.ans3 = form.ans3.data
        tasks.ans4 = form.ans4.data
        tasks.correct_answer = form.correct_answer.data
        tasks.test_id = num
        session.add(tasks)
        session.commit()
        if COUNT_OF_OTHER_QUESTIONS > 1:
            COUNT_OF_OTHER_QUESTIONS -= 1
            return redirect('/task')
        else:
            return redirect('/school')
    return render_template('task.html', title='Добавление вопроса', form=form)


@app.route('/test_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def tests_delete(id):
    session = db_session.create_session()
    sess = db_session.create_session()
    tests = session.query(Tests).filter(Tests.id == id, Tests.user == current_user).first()
    tasks = sess.query(Tasks).filter(Tasks.test_id == id)
    ses = db_session.create_session()
    res = ses.query(Answers).filter(Answers.test_id == id)
    if tests:
        session.delete(tests)
        session.commit()
        for task in tasks:
            sess.delete(task)
            sess.commit()
        for result in res:
            ses.delete(result)
            ses.commit()
    else:
        abort(404)
    return redirect('/school')


points = 0


@app.route('/test/<int:id>/<int:n_task>', methods=['GET', 'POST'])
@login_required
def write_test(id, n_task):
    global questions, points
    session = db_session.create_session()
    test = session.query(Tests).filter(Tests.id == id)
    for tes in test:
        sess2 = db_session.create_session()
        tasks = sess2.query(Tasks).filter(Tasks.test_id == id)
        t = tasks[n_task]
        form = AnserForm()
        if n_task == 0:
            points = 0
        if form.validate_on_submit():
            if request.method == 'POST':
                if 'task' in request.form:
                    users_answer = request.form['task']
                    if int(users_answer) == int(t.correct_answer):
                        points += 1
            if int(tes.count_of_questions) > (n_task + 1):
                n_task += 1
                return redirect(f'/test/{id}/{n_task}')
            else:
                print(points)
                return redirect(f'/result/{tes.id}/{tes.title}/{points}/{tes.count_of_questions}')

        return render_template("testwriting.html", test=tes, tasks=t, id=id, form=form, cou=int(tes.count_of_questions),
                               n=n_task)


@app.route('/result/<int:id>/<title>/<int:points>/<int:max>', methods=['GET', 'POST'])
@login_required
def result(id, title, points, max):
    session = db_session.create_session()
    ans = Answers()
    ans.title = title
    ans.test_id = id
    ans.user = f'{current_user.name} {current_user.clas}'
    ans.points = points
    ans.max_points = max
    session.add(ans)
    session.commit()
    return render_template('result.html', points=points, max=max)


@app.route('/result_test/<int:id>', methods=['GET', 'POST'])
@login_required
def tests_result(id):
    session = db_session.create_session()
    ans = session.query(Answers).filter(Answers.test_id == id).all()
    tes = ans[0]
    return render_template('results.html', ans=ans, test=tes)


if __name__ == '__main__':
    app.run(port=8082, host='127.0.0.1')
