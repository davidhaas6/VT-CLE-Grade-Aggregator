from xml.dom import minidom
from pprint import pprint
import pickle

f = open('area_2_cles.p', 'r')
df = pickle.load(f)
f.close()

# for i in range(len(df)):
#    print str(df['#'][i]) + '\t\t' + str(df['COURSE_TITLE'][i])

cle_courses = []
NULL = 'nan'

# Sorts the CLE Course data into an list of dicts, filters out classes with prerequisites
for i in range(len(df)):
    prereqs = str(df['PREREQUISTES'][i])
    subject = str(df['SUBJ'][i])
    course_num = str(df['#'][i])
    title = str(df['COURSE_TITLE'][i])

    if prereqs == NULL and title != NULL:
        # If the title is 2 lines on the pdf, this concatenates the second line onto the first
        if course_num == NULL:
            cle_courses[len(cle_courses) - 1]['title'] += ' ' + title
        # Otherwise, adds the course to the list
        else:
            cle_courses.append({'subject_num': subject + course_num, 'title': title})

# pprint(cle_courses)

xml_doc = minidom.parse('grade_distribution.xml')
xml_course_list = xml_doc.getElementsByTagName('Detail')
master_course_list = dict()

for course in xml_course_list:
    attr = course.attributes
    # Concatenates the subj+number ex: HIST1204
    subject_concat_number = str(attr['department'].value + attr['course_number_1'].value)
    course_data = {'gpa': round(float(attr['qca'].value), 4),
                   'As': round(float(attr['As'].value), 4),
                   'teacher': str(attr['faculty'].value)}
    if subject_concat_number not in master_course_list:
        master_course_list[subject_concat_number] = [course_data]
    else:
        master_course_list[subject_concat_number] += [course_data]

# print len(master_course_list)

'''
user_in = ''
while user_in != 'stop':
    user_in = raw_input('\n\nEnter subject + course number (ex: HIST1204): ').upper()
    try:
        print master_course_list[user_in]
    except KeyError:
        print "Error: " + user_in + " not found"
'''
formatted_course_list = dict()
formatted_course_list['raw'] = master_course_list
stats_dict = dict()

for course_name, data in master_course_list.items():
    avg_percent = 0.0
    avg_gpa = 0.0
    highest_percent = 0.0
    highest_teacher = ''
    for class_data in data:
        percent_a = class_data['As']
        avg_percent += percent_a
        avg_gpa += class_data['gpa']
        if percent_a > highest_percent:
            highest_percent = percent_a
            highest_teacher = class_data['teacher']
    avg_percent /= len(data)
    avg_gpa /= len(data)
    stats_dict[course_name] = {'avg %As': avg_percent, 'highest %As': [highest_percent, highest_teacher],
                               'avg gpa': avg_gpa}
formatted_course_list['stats'] = stats_dict
# print formatted_course_list['stats']
count = 0
for course in cle_courses:
    course_name = course['subject_num']
    if course_name in formatted_course_list['stats']:
        course.update(formatted_course_list['stats'][course_name])
    else:
        course.update({'avg %As': -1, 'highest %As': [-1, 'nan'], 'avg gpa': -1})

# pprint(cle_courses)

sorted_course_list = sorted(cle_courses, key=lambda k: k['avg %As'])
sorted_course_list.reverse()
# pprint(sorted_course_list)

for course in sorted_course_list[:30]:
    print 'Title:\t\t', course['subject_num'] + ' ' + course['title']
    print 'Avg %A:\t\t', course['avg %As']
    print 'Avg GPA:\t', course['avg gpa']
    print 'Highest %A:', str(course['highest %As'][0]) + ',', course['highest %As'][1]
    print ''
