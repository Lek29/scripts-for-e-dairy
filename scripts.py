from datacenter.models import Schoolkid, Mark, Chastisement, Subject, Lesson, Commendation
from random import choice


def get_schoolkid(full_name):
    try:
        return Schoolkid.objects.get(full_name=full_name)
    except Schoolkid.DoesNotExist:
        raise ValueError(f"Ученик с ФИО '{full_name}' не найден.")
    except Scoolkid.MultipleObjectsReturned:
        raise ValueError(f"Найдено несколько учеников с ФИО '{full_name}'. Уточните ФИО.")


def fix_marks(name):
    try:
        student_name = get_schoolkid(name)
    except ValueError as e:
        print(e)
        return

    bad_marks = Mark.objects.filter(schoolkid_id=student_name.id, points__in=[2, 3])
    if not bad_marks.exists():
        print(f'У ученика {name} нет плохих оценок')
        return

    bad_marks.update(points=choice([4, 5]))
    print(f'Оценки ученика {name} успешно исправлены!')


def remove_chastisements(schoolkid):
    try:
        student = get_schoolkid(schoolkid)
    except ValueError as e:
        print(e)
        return

    Chastisement.objects.filter(schoolkid=student).delete()


def create_commendation(full_name, subject_title):
    try:
        schoolkid = get_schoolkid(full_name)
    except ValueError as e:
        print(e)
        return

    try:
        subject = Subject.objects.get(title=subject_title, year_of_study=schoolkid.year_of_study)
    except Subject.DoesNotExist:
        print(f"Предмет с названием '{subject_title}' не найден.")
        return
    except Subject.MultipleObjectsReturned:
        print(f"Найдено несколько предметов с названием '{subject_title}'. Уточните название.")
        return

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
