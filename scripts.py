from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from datacenter.models import Schoolkid, Mark, Chastisement, Subject, Lesson, Commendation
from random import choice

def fix_marks(name):
    student_name = Schoolkid.objects.filter(full_name__contains=name).first()
    if not student_name:
        print(f'Ученик с именем {name} не найден')
        return
    bad_marks = Mark.objects.filter(schoolkid_id=student_name.id, points__in=[2, 3])
    if not bad_marks.exists():
        print(f'У ученика {name} нет плохих оценок')
        return
    for mark in bad_marks:
        mark.points = choice([4, 5])
        mark.save()
    print(f'Оценки ученика {name} успешно исправлены!')


def remove_chastisements(schoolkid):
    student_name = Schoolkid.objects.filter(full_name__contains=schoolkid)[0]
    student_chastisement = Chastisement.objects.filter(schoolkid=student_name)
    for chastisement in student_chastisement:
        chastisement.delete()


def create_commendation(full_name, subject_title):
    try:
        schoolkid = Schoolkid.objects.get(full_name=full_name)
    except ObjectDoesNotExist:
        print(f"Ученик с ФИО '{full_name}' не найден.")
        return
    except MultipleObjectsReturned:
        print(f"Найдено несколько учеников с ФИО '{full_name}'. Уточните ФИО.")
        return

    subject = Subject.objects.filter(title=subject_title, year_of_study=schoolkid.year_of_study).first()

    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
    ).order_by('-date')
    if not lessons.exists():
        print(f"Уроки по предмету '{subject_title}' для ученика '{full_name}' не найдены.")
        return
    last_lesson = lessons.first()

    commendation_text = [
        'Отличная работа!',
        'Прекрасное начало!',
        'Здорово!',
        'Ты на верном пути',
        'Ты растешь над собой!',
    ]

    Commendation.objects.create(
        text=choice(commendation_text),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=last_lesson.teacher
    )
    print(f"Похвала для ученика '{full_name}' по предмету '{subject_title}' успешно создана.")
