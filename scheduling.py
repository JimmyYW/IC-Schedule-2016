from app.models import Course, SectionToTime, Time, Section
import copy

"""
ALGORITHM
1. Create a dictionary of dictionary of lists (course to section to times)
2. Do a double loop to compare classes: i = (0, len(dict.keys())-1) and j = (i, len(dict.keys())
3. Each loop goes from 0 to len(dict[coursename]).keys())-1 (i.e. num of sections)
4. Compare times for sections.
    - If there are no conflicts, add a tuple of sections to a list???
        - FOR NOW: Just break and display one schedule that works, you nincompoop.
    - If there are conflicts, continue.
5. At the end of the outer loop, you have a shit.

TAKE TWO

1. Still with the dictionary of dictionaries of lists. I think.
2. Pick the first section from each.
    -If it time work, display it
    -If it don't, don't
3. Increment a section, rinse, repeat

Comparing and looping with an unknown number of classes is going to be tricky, but I'm going to launch right in.

A BETTER FORMAT for organizing things with multiple data structures:
1. course list (comes straight from selected classes)
2. course:section dict of lists
3. section:time dict of lists
"""


def make_selected_dict(courses):
    selected = dict()
    for c in courses:
        sections = Section.query.filter_by(courseId=c.id)
        selected[c] = list()
        for s in sections:
            s2ts = SectionToTime.query.filter_by(sectionId=s.id)
            times = list()
            for s2t in s2ts:
                times.append(Time.query.get(s2t.timeId))
            selected[c].append({s: times})
    return selected


class Schedulizer:
    def __init__(self, clist):
        self.clist = clist
        self.cdict, self.sdict = self.make_dicts()
        self.sched_list = list()

    def make_dicts(self):
        course_dict = dict()
        section_dict = dict()
        for c in self.clist:
            sectionlist = Section.query.filter_by(courseId=c.id)
            course_dict[c] = list()
            for s in sectionlist:
                course_dict[c].append(s)
                s2ts = SectionToTime.query.filter_by(sectionId=s.id)
                timelist = list()
                for s2t in s2ts:
                    timelist.append(Time.query.get(s2t.timeId))
                section_dict[s] = timelist
        return course_dict, section_dict

    def find_conflicts(self, s1, s2):
        times1 = self.sdict[s1]
        times2 = self.sdict[s2]
        invalid = False
        for t1 in times1:
            for t2 in times2:
                if has_conflict(t1, t2):
                    invalid = True
                    break
            if invalid:
                break
        return invalid

    def get_section_from_idx(self, cidx, i):
        course = self.clist[cidx]
        return self.cdict[course][i]

    def check_all_sections(self, current_idcs):
        valid = True
        schedule = list()
        for i in range(len(self.clist)-1):
            for j in range(i+1, len(self.clist)):
                s1 = self.get_section_from_idx(i, current_idcs[i])
                s2 = self.get_section_from_idx(j, current_idcs[j])
                if self.find_conflicts(s1, s2):
                    # print("Schedule "+str(current_idcs)+" is invalid; "
                    #       "sections "+str(s1)+" and "+str(s2)+" conflict.")
                    valid = False
                    break

            if not valid:
                break
            # at this point, section at i has been tested against all other sections and is valid.
            schedule.append(self.get_section_from_idx(i, current_idcs[i]))
        if valid:
            # add that one last section that was good to schedule; couldn't be done before.
            schedule.append(self.get_section_from_idx(len(self.clist)-1, current_idcs[len(self.clist)-1]))
            # print("Good schedule: "+str(schedule))
            self.sched_list.append(schedule)

    def recursive_looping_sucks(self, maxes, current_idcs):
        if len(maxes) == 0:
            self.check_all_sections(current_idcs)
        else:
            for i in range(maxes[0]):
                if current_idcs is None:
                    new_idcs = [i]
                else:
                    new_idcs = list(current_idcs)
                    new_idcs.append(i)
                self.recursive_looping_sucks(maxes[1:], new_idcs)

    def generate_schedules(self):
        # how do i dynamically generate enough for loops for this nonsense
        # stack overflow tells me to be hacky and recursive. say no more, stack overflow
        maxes = [len(self.cdict[c]) for c in self.clist]
        self.recursive_looping_sucks(maxes, list())


def has_conflict(time1, time2):
    # DID YOU KNOW YOU CAN CHAIN BOOLEAN EXPRESSIONS LIKE THIS IN PYTHON????? MY MATH BRAIN IS SO SATISFIED
    if (time1.timeStart <= time2.timeStart <= time1.timeEnd or time2.timeStart <= time1.timeStart <= time2.timeEnd)\
            and (time1.day == time2.day):
        return True
    else:
        return False


def main():
    clist = Course.query.all()
    sch = Schedulizer(clist)
    sch.generate_schedules()
    print(sch.sched_list)

if __name__ == "__main__":
    main()

