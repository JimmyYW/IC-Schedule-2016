import os
from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from app.models import Dept, Course, Section

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "The peperonizzi always try photogreph me in compromisin position. Unlucky for them" \
                           "my head will be soon unstuck from this sodacan. Any minut"
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


@app.route('/')
def index():
    deptList = Dept.query.order_by('name')
    courseList = Course.query.order_by('name')
    sectionList = Section.query.order_by('id')
    return render_template('templates/index.html', depts=deptList, courses=courseList, sections=sectionList)


def main():
    manager.run()


if __name__ == "__main__":
    main()

