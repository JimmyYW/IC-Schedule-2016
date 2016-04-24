from app import app
from app.models import Dept, Course, Section, SectionToTime
from flask import render_template, session, redirect, url_for
from scheduling import Schedulizer



@app.route('/new')
def new():
    return render_template('newbase.html')


@app.route('/')
def landing():
    return render_template('landing.html')





@app.route('/index')
def index():
    deptList = Dept.query.order_by('name')
    courseList = Course.query.order_by('name')
    sectionList = Section.query.order_by('id')
    return render_template('index.html', depts=deptList, courses=courseList, sections=sectionList)


@app.route('/schedule')
def schedule():
    clist = Course.query.all()
    sch = Schedulizer(clist)
    sch.generate_schedules()
    return render_template('schedule.html', sch=sch)
