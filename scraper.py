from app import db
from app.models import Course, Dept, Section, SectionToTime, Time
from bs4 import BeautifulSoup
from datetime import datetime


__author__ = 'KSADWIN'


NUM_CELLS_PER_ROW = 20
INDEX_CRN = 1
INDEX_DEPT = 2
INDEX_COURSENUM = 3
INDEX_CREDITS = 6
INDEX_NAME = 7
INDEX_DAYS = 8
INDEX_TIMES = 9
INDEX_PROF = 16
INDEX_DATES = 17
INDEX_ROOM = 18
INDEX_ATTRS = 19  # notes such as ICC credit info. no proper description given on table, use this instead?


def get_dept(name, abbr):
    """
    Finds or creates row in db for dept. Searches by abbr for lookup, as it should be a unique identifier.
    :param name: string full name (i.e. Computer Science)
    :param abbr: string abbreviated name (i.e. COMP)
    :return: dept object
    """
    d = Dept.query.filter_by(abbr=abbr).first()
    if d is None:
        # make dept and commit to db
        d = Dept(name, abbr)
        db.session.add(d)
        db.session.commit()
    return d


def get_course(dept, num, name, credits, desc):
    """
    Finds or creates row in db for course. Searches by dept and num for lookup, as they should be unique identifiers.
    :param dept: row in Dept table
    :param num: int course number
    :param name: course name
    :param credits: double credit count (note to past self: why did you make it an int)
    :param desc: string description
    :return: course object
    """
    c = Course.query.filter_by(deptId=dept.id, number=num).first()
    if c is None:
        c = Course(name, desc, num, credits, dept)
        db.session.add(c)
        db.session.commit()
    return c


def get_section(course, prof, crn):
    """
    Finds or creates row in db for section. Searches by crn for lookup, as it should be a unique identifier.
    Note: Finding an existing section in the db means that this table has been parsed before.
    :param course: row in Course table
    :param prof: string professor name, or TBA
    :param crn: int CRN
    :return: section object
    """
    s = Section.query.filter_by(crn=crn).first()
    if s is None:
        s = Section(crn, prof, course)
        db.session.add(s)
        db.session.commit()
    return s


def get_db_items_from_listing(row):
    """
    Creates or finds the necessary database objects for a course listing.
    A plethora of constant ints are defined at the beginning of the file to self-document code.
    :param row: a tr tag from the table of classes. may not contain td elements, must check
    :return: section object
    """
    cells = row.find_all("td")
    if len(cells) != NUM_CELLS_PER_ROW:
        return

    # TODO: Find full name for dept. This creates dept objects that read COMP, COMP rather than Computer Science, COMP.
    dept = get_dept(cells[INDEX_DEPT].get_text(), cells[INDEX_DEPT].get_text())

    # TODO: Get full description for course. Currently uses ICC credit info.
    # Variable credits are stored as -1 in a dirty fix.
    try:
        credit = float(cells[INDEX_CREDITS].get_text())
    except ValueError:
        credit = -1
    course = get_course(dept, int(cells[INDEX_COURSENUM].get_text()), cells[INDEX_NAME].get_text(),
                        credit, cells[INDEX_ATTRS].get_text())

    section = get_section(course, cells[INDEX_PROF].get_text(), int(cells[INDEX_CRN].get_text()))

    times = get_times_from_cells(cells)

    if times is None:
        return section

    s2ts = get_section_to_time(section, times)

    return section


def get_section_to_time(section, times):
    """
    Creates or finds row in db for SectionToTimes. If existing rows are found, no further work is necessary.
    :param section: section object from db
    :param times: list of time objects from db
    :return: list of SectionToTime objects
    """
    s2ts = SectionToTime.query.filter_by(sectionId=section.id).all()
    if len(s2ts) > 0:
        return s2ts
    s2ts = []
    for t in times:
        s2ts.append(SectionToTime(section, t))

    db.session.add_all(s2ts)
    db.session.commit()
    return s2ts


def get_times_from_cells(cells):
    """
    Creates or finds row in db for times. All cells are passed for ease of reuse as this function is called by both
    get_db_items_from_listing() and scrape_web().
    :param cells: list of BeautifulSoup td elements, should have length 20
    :return: list of time objects
    """
    days = cells[INDEX_DAYS].get_text()
    times = cells[INDEX_TIMES].get_text().split("-")

    try:
        starttime = datetime.strptime(times[0], "%I:%M %p").time()
        endtime = datetime.strptime(times[1], "%I:%M %p").time()

        times = []

        for d in days:
            if d == "U":
                d = 0
            elif d == "M":
                d = 1
            elif d == "T":
                d = 2
            elif d == "W":
                d = 3
            elif d == "R":
                d = 4
            elif d == "F":
                d = 5
            else:
                d = 6
            t = Time.query.filter_by(timeStart=starttime, timeEnd=endtime, day=d).first()
            if t is None:
                t = Time(starttime, endtime, d)
                db.session.add(t)
                db.session.commit()
            times.append(t)

        return times

    except ValueError:
        # occurs when time is TBA
        return None


def scrape_web(html):
    """
    Populates database with courses given the proper homerconnect page full of courses (Look Up Classes).
    :param html: the html to scrape, as a string. allows scraping of local or remote html
    :return: probably none, just commits to db here. we'll see.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="datadisplaytable")
    rows = table.find_all("tr")
    section = None
    for r in rows:
        # catch sparse rows, which add times to previously accessed section
        if r.get_text().startswith("\n\xa0\n\xa0\n\xa0\n\xa0"):
            times = get_times_from_cells(r.find_all("td"))
            if times is not None:
                get_section_to_time(section, times)
        else:
            section = get_db_items_from_listing(r)


def main():
    file = open("ALLtheclasses.html")
    scrape_web(file.read())


if __name__ == "__main__":
    main()
