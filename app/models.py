from app import db
import datetime as dt


class Dept(db.Model):
    __tablename__ = 'dept'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    abbr = db.Column(db.String(4))

    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr

    def __repr__(self):
        return "<Dept %r>" % self.abbr


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    desc = db.Column(db.String(256))
    number = db.Column(db.Integer)
    credits = db.Column(db.Integer)
    deptId = db.Column(db.Integer, db.ForeignKey('dept.id'))

    dept = db.relationship('Dept', foreign_keys=deptId)

    def __init__(self, name, desc, number, credits, dept):
        self.name = name
        self.desc = desc
        self.number = number
        self.credits = credits
        self.dept = dept

    def __repr__(self):
        return "<Course %r>" % self.name


class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    crn = db.Column(db.Integer)
    prof = db.Column(db.String(64))
    courseId = db.Column(db.Integer, db.ForeignKey('course.id'))

    course = db.relationship('Course', foreign_keys=courseId)

    def __init__(self, crn, prof, course):
        self.crn = crn
        self.prof = prof
        self.course = course

    def __repr__(self):
        return "<Section %r>" % self.crn


class Time(db.Model):
    __tablename__ = 'time'
    id = db.Column(db.Integer, primary_key=True)
    timeStart = db.Column(db.Time)
    timeEnd = db.Column(db.Time)
    day = db.Column(db.Integer)  # 0=Sunday, 6=Saturday

    def __init__(self, start, end, day):
        self.timeStart = start
        self.timeEnd = end
        self.day = day

    def __repr__(self):
        return "<Time %r>" % self.id


class SectionToTime(db.Model):
    __tablename__ = 'section2time'
    id = db.Column(db.Integer, primary_key=True)
    timeId = db.Column(db.Integer, db.ForeignKey('time.id'))
    sectionId = db.Column(db.Integer, db.ForeignKey('section.id'))

    time = db.relationship('Time', foreign_keys=timeId)
    section = db.relationship('Section', foreign_keys=sectionId)

    def __init__(self, section, time):
        self.time = time
        self.section = section

    def __repr__(self):
        return "<SectionToTime %r>" % self.id


def populate_db():
    """
    dept = Dept("Computer Science", "COMP")
    course = Course("Adv. Web", "Doug rocks", 20500, 4, dept)
    section = Section(12345, "Doug", course)
    time = Time(dt.time(14, 0), dt.time(14, 50), 1)
    section2time = SectionToTime(section, time)
    db.session.add(dept)
    db.session.add(course)
    db.session.add(section)
    db.session.add(time)
    db.session.add(section2time)

    deptcs = Dept.query.get(1)
    course171 = Course("Principles I", "Learn Python", 17100, 4, deptcs)
    course172 = Course("Principles II", "Learn Java", 17200, 4, deptcs)
    section171_1 = Section(17101, "Paul", course171)
    section171_2 = Section(17102, "John", course171)
    section172 = Section(17201, "Toby", course172)
    time11m = Time(dt.time(11, 0), dt.time(11, 50), 1)
    time11w = Time(dt.time(11, 0), dt.time(11, 50), 3)
    time1m = Time(dt.time(13, 0), dt.time(13, 50), 1)
    time1w = Time(dt.time(13, 0), dt.time(13, 50), 3)
    time2m = Time.query.get(1)
    time2w = Time(dt.time(14, 0), dt.time(14, 50), 3)
    s2t_17101_11m = SectionToTime(section171_1, time11m)
    s2t_17101_11w = SectionToTime(section171_1, time11w)
    s2t_17102_2m = SectionToTime(section171_2, time2m)
    s2t_17102_2w = SectionToTime(section171_2, time2w)
    s2t_17201_1m = SectionToTime(section172, time1m)
    s2t_17201_1w = SectionToTime(section172, time1w)
    db.session.add_all([course171, course172, section171_1, section171_2, section172, time11m, time11w, time1m, time1w,
                       time2w, s2t_17101_11m, s2t_17101_11w, s2t_17102_2m, s2t_17102_2w, s2t_17201_1m, s2t_17201_1w])
    db.session.commit()
    """


def main():
    populate_db()


if __name__ == "__main__":
    main()

