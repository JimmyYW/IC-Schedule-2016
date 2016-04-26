from app import app
from flask import json
from flask import request
from flask import jsonify
from app.models import Dept, Course, Section, SectionToTime,Time
from flask import render_template, session, redirect, url_for
from scheduling import Schedulizer

@app.route('/_load_section')
def load_section():
    courseIdIn = request.args.get('getcourseId',type=int)
    sectionList = Section.query.order_by('id')
    courseList = Course.query.order_by('id')
    listOfSectionsCRN =[]
    listOfSectionsProf =[]
    listOfSectionTimeStart = []
    listOfSectionTimeEnd = []
    listOfSectionTimeDay = []
    courseDesc =""
    courseNum =0
    courseCred=0.0
    courseIdOut =0;
    courseName ="";
    ## i can do better use filter by but im tired now so ... no
    for s in sectionList:
        if s.courseId == courseIdIn:
            listOfSectionsCRN.append(s.crn)
            listOfSectionsProf.append(s.prof)
            s2ts = SectionToTime.query.filter_by(sectionId=s.id)
            for s2t in s2ts:
                listOfSectionTimeStart.append([Time.query.get(s2t.timeId).timeStart.hour,Time.query.get(s2t.timeId).timeStart.minute])
                listOfSectionTimeEnd.append([Time.query.get(s2t.timeId).timeStart.hour,Time.query.get(s2t.timeId).timeStart.minute])
                listOfSectionTimeDay.append(Time.query.get(s2t.timeId).day)

    for c in courseList:
        if c.id == courseIdIn:
            courseDesc=c.desc
            courseNum=c.number
            courseCred=c.credits
            courseName=c.name
            courseIdOut = c.id

    return jsonify(listOfSectionsCRNOut = listOfSectionsCRN, listOfSectionsProfOut = listOfSectionsProf, listOfSectionTimeStartOut = listOfSectionTimeStart, listOfSectionTimeEndOut= listOfSectionTimeEnd, listOfSectionTimeDayOut = listOfSectionTimeDay, courseDescOut=courseDesc, courseNumOut=courseNum, courseCredOut=courseCred, courseName=courseName, courseIdOut=courseIdOut  )

@app.route('/_load_list')
def add_numbers():
    deptIdIn = request.args.get('deptIdIn',type=int)
    courseList = Course.query.order_by('name')
    cListByDept =[]
    cListByDeptId =[]
    for c in courseList:
        if c.deptId == deptIdIn:
            cListByDept.append(c.name)
            cListByDeptId.append(c.id)

    return jsonify(listByDept = cListByDept, listByDeptId = cListByDeptId)



@app.route('/new')
def new():
    deptList = Dept.query.order_by('name')
    return render_template('newbase.html', depts=deptList)


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
