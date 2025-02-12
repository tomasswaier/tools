import copy
from datetime import time, datetime

classes = {
    "PAS": [[1, [time(14, 0), time(15, 50)]], [1, [time(16, 0), time(17, 50)]],
            [2, [time(14, 0), time(15, 50)]], [2, [time(16, 0), time(17, 50)]],
            [3, [time(10, 0), time(11, 50)]], [3, [time(12, 0), time(13, 50)]],
            [3, [time(16, 0), time(17, 50)]], [3, [time(18, 0), time(19, 50)]]],
    "DBS": [[2, [time(11, 0), time(12, 50)]], [3, [time(10, 0), time(11, 50)]],
            [3, [time(12, 0), time(13, 50)]], [3, [time(16, 0), time(17, 50)]],
            [4, [time(9, 0), time(10, 50)]], [4, [time(11, 0), time(12, 50)]]],
    "TEAP": [[4, [time(8, 0), time(9, 50)]], [4, [time(10, 0), time(11, 50)]],
             [4, [time(12, 0), time(13, 50)]], [4, [time(14, 0), time(15, 50)]]],
    "PSI": [[1, [time(14, 0), time(15, 50)]], [1, [time(16, 0), time(17, 50)]],
            [1, [time(18, 0), time(19, 50)]], [2, [time(11, 0), time(12, 50)]],
            [2, [time(14, 0), time(15, 50)]], [2, [time(16, 0), time(17, 50)]],
            [2, [time(18, 0), time(19, 50)]], [4, [time(9, 0), time(10, 50)]],
            [4, [time(11, 0), time(12, 50)]]],
    "PIS": [[3, [time(14, 0), time(15, 50)]], [3, [time(16, 0), time(17, 50)]],
            [3, [time(18, 0), time(19, 50)]], [4, [time(9, 0), time(10, 50)]],
            [4, [time(11, 0), time(12, 50)]], [4, [time(14, 0), time(15, 50)]]],
    "SPAASM": [[1, [time(16, 0), time(17, 50)]], [1, [time(18, 0), time(19, 50)]],
               [3, [time(16, 0), time(17, 50)]], [3, [time(18, 0), time(19, 50)]]]
}

seminars = {
    "PAS": [
        {
            "day": 1,     # Example date (year, month, day)
            "start_time": [time(8, 0), time(12, 50)],       # Start time: 8:00 AM
        }
    ],
    "DBS": [
        {
            "day": 2,     # Example date (year, month, day)
            "start_time": [time(9, 0), time(10, 50)],       # Start time: 8:00 AM
        }],
    "TEAP": [
        {
            "day": 2,     # Example date (year, month, day)
            "start_time": [time(18, 0), time(19, 50)],       # Start time: 8:00 AM
        }],
    "PSI": [
        {
            "day": 4,     # Example date (year, month, day)
            "start_time": [time(16, 0), time(18, 50)],       # Start time: 8:00 AM
        }],
    "PIS": [
        {
            "day": 3,     # Example date (year, month, day)
            "start_time": [time(11, 0), time(12, 50)],       # Start time: 8:00 AM
        }],
    "SPAASM": [
        {
            "day": 1,     # Example date (year, month, day)
            "start_time": [time(13, 0), time(15, 50)],       # Start time: 8:00 AM
        }]
}


def time_difference(time1, time2):
    """Calculates the difference in minutes between two time objects."""
    dt1 = datetime.combine(datetime.min, time1)
    dt2 = datetime.combine(datetime.min, time2)
    return (dt1 - dt2).total_seconds() / 60


def evaluate_class(class_time, timetable_day):
    result_evaluation = -1
    for set_class in timetable_day:
        set_class_start_time = set_class[1][0]
        set_class_end_time = set_class[1][1]
        print("comparing ", set_class_start_time, set_class_end_time, class_time[0], class_time[1])
        if set_class_start_time <= class_time[0] and class_time[1] <= set_class_end_time:
            return -1
        else:
            if set_class_start_time > class_time[1]:
                result_evaluation = time_difference(set_class_start_time, class_time[1])
            if set_class_end_time < class_time[0]:
                result_evaluation = time_difference(class_time[0], set_class_end_time)
    if len(timetable_day) == 0:
        return 300
    return result_evaluation


def evaluate_all_class(timetable):
    result_array = []
    for class_name in classes:
        for class_time in classes[class_name]:
            evaluation = evaluate_class(class_time[1], timetable[class_time[0] - 1])
            if evaluation != -1:
                result_array.append([evaluation, class_name, class_time])
    return result_array


def run_combinations(timetable, class_list):
    evaluated_classes = sorted(evaluate_all_class(timetable))
    class_list_copy = copy.copy(class_list)
    print(evaluated_classes)
    for evaluation in evaluated_classes:
        # print(evaluation)
        if evaluation[1] in class_list_copy:
            if evaluate_class(evaluation[2][1], timetable[evaluation[2][0] - 1]) == - 1:
                continue
            timetable[evaluation[2][0] - 1].append([evaluation[1], evaluation[2][1]])
            class_list_copy.remove(evaluation[1])
            if not class_list_copy:
                return timetable
    # after evaluation i go to combinations based off of lowest evaluated classes
    print("couldn't set all classes ", class_list_copy)
    return timetable


def print_timetable(timetable):
    for i, day in enumerate(timetable):
        day = sorted(day, key=lambda x: x[1][0])
        day_string = str(i) + "|"
        for subject in day:
            day_string += f"{subject[0]}:{subject[1][0].strftime('%H:%M')}-{subject[1][1].strftime('%H:%M')}|"
        print(day_string)


def main():
    timetable = [[], [], [], []]
    class_list = []
    # added seminars that can't be changed
    for class_name in seminars:
        class_list.append(class_name)
        class_info = seminars[class_name]
        timetable[class_info[0]["day"] - 1].append([class_name, class_info[0]["start_time"]])
        timetable[class_info[0]["day"] - 1].sort()
    result_timetable = run_combinations(timetable, class_list)
    print_timetable(result_timetable)


main()

