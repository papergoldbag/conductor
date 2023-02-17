from datetime import datetime

from conductor.core.misc import db
from conductor.db.models import UserDBM, Roles, DivisionDBM, RoadmapDBM, TaskDBM, TaskTypes, QuizDBM


def insert_test_data():
    db.drop()

    division1 = DivisionDBM.parse_document(
        db.division.insert_document(DivisionDBM(title='РЕМЦ').document())
    )
    division2 = DivisionDBM.parse_document(
        db.division.insert_document(DivisionDBM(title='Роскультцентр').document())
    )
    division3 = DivisionDBM.parse_document(
        db.division.insert_document(DivisionDBM(title='Роспатриот').document())
    )
    division3 = DivisionDBM.parse_document(
        db.division.insert_document(DivisionDBM(title='ЦСМС').document())
    )

    roadmap1 = RoadmapDBM.parse_document(
        db.roadmap.insert_document(RoadmapDBM(
            title='',
            tasks=[
                TaskDBM(
                    type=TaskTypes.auto_test,
                    title='Прочитайте данные статьи',
                    text='Прочитайте данные статьи и пройдите тест ниже',
                    is_confirmed_by_hr_int_id=123,
                    coins=12,
                    is_completed=False,
                    attachments={"Наш сайт": "http://rscenter.ru/"},
                    quizzes=[
                        QuizDBM(
                            question='Первая буква алфавита ?',
                            answer=None,
                            correct_answer='A'
                        ),
                        QuizDBM(
                            question='Вторая буква алфавита ?',
                            answer=None,
                            correct_answer='Б'
                        )
                    ]
                ),
                TaskDBM(
                    type=TaskTypes.hr_confirmation,
                    title='Подпишите документы',
                    text='Требуется придти и подписать документы',
                    is_confirmed_by_hr_int_id=123,
                    coins=15,
                    is_completed=False,
                    attachments={},
                    quizzes=[]
                ),
                TaskDBM(
                    type=TaskTypes.feedback,
                    title='Дайте обратную связь о том, как провели данный день',
                    text='Нужно пройти опрос ниже )',
                    is_confirmed_by_hr_int_id=123,
                    coins=15,
                    is_completed=False,
                    attachments={},
                    quizzes=[
                        QuizDBM(
                            question='Всё было хорошо ?',
                            answer=None,
                            correct_answer=None
                        )
                    ]
                )
            ],
            created_by_int_id=123
        ).document())
    )

    roadmap2 = RoadmapDBM.parse_document(
        db.roadmap.insert_document(RoadmapDBM(
            title='',
            tasks=[
                TaskDBM(
                    type=TaskTypes.auto_test,
                    title='Прочитайте данные статьи',
                    text='Прочитайте данные статьи и пройдите тест ниже',
                    is_confirmed_by_hr_int_id=123,
                    coins=12,
                    is_completed=False,
                    attachments={"Наш сайт": "http://rscenter.ru/"},
                    quizzes=[
                        QuizDBM(
                            question='Первая буква алфавита ?',
                            answer=None,
                            correct_answer='A'
                        ),
                        QuizDBM(
                            question='Вторая буква алфавита ?',
                            answer=None,
                            correct_answer='Б'
                        )
                    ]
                ),
                TaskDBM(
                    type=TaskTypes.hr_confirmation,
                    title='Подпишите документы',
                    text='Требуется придти и подписать документы',
                    is_confirmed_by_hr_int_id=123,
                    coins=15,
                    is_completed=False,
                    attachments={},
                    quizzes=[]
                ),
                TaskDBM(
                    type=TaskTypes.feedback,
                    title='Дайте обратную связь о том, как провели данный день',
                    text='Нужно пройти опрос ниже )',
                    is_confirmed_by_hr_int_id=123,
                    coins=15,
                    is_completed=False,
                    attachments={},
                    quizzes=[
                        QuizDBM(
                            question='Всё было хорошо ?',
                            answer=None,
                            correct_answer=None
                        )
                    ]
                )
            ],
            created_by_int_id=123
        ).document())
    )

    db.user.insert_document(UserDBM(
        fullname='https://vk.com/ilyakhakimov03',
        email='ilyakhakimov03@gmail.com',
        tokens=[],
        role=Roles.employee.value,
        coins=0,
        position='HTML/CSS/JS developer',
        birth_date=datetime(year=2003, month=3, day=27),
        description='ZZZ',
        telegram='asf',
        whatsapp='asf',
        vk='asf',
        roadmap_int_id=roadmap1.int_id,
        division_int_id=division1.int_id
    ).document())

    db.user.insert_document(UserDBM(
        fullname='Денис',
        email='dbarov3@gmail.com',
        tokens=[],
        role=Roles.employee.value,
        coins=0,
        position='Android Developer',
        birth_date=datetime(year=2003, month=3, day=27),
        description='Я занимаюсь разработкой около 3 лет и мне это нравится',
        telegram='asf',
        whatsapp='asf',
        vk='https://vk.com/brightos',
        roadmap_int_id=roadmap2.int_id,
        division_int_id=division2.int_id
    ).document())


insert_test_data()
