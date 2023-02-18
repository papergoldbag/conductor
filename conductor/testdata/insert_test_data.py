from datetime import datetime, timedelta

from conductor.core.misc import db
from conductor.db.models import UserDBM, Roles, DivisionDBM, RoadmapDBM, TaskDBM, TaskTypes, QuizDBM, Attachment, \
    EventDBM


def insert_test_data():
    db.drop()
    for collection in db.database.list_collections():
        db.database.get_collection(collection.get('name')).drop()

    division1 = DivisionDBM.parse_document(
        db.division.insert_document(DivisionDBM(title='РЕМЦ').document())
    )
    division2 = DivisionDBM.parse_document(
        db.division.insert_document(DivisionDBM(title='Роскультцентр').document())
    )
    division3 = DivisionDBM.parse_document(
        db.division.insert_document(DivisionDBM(title='Роспатриот').document())
    )
    division4 = DivisionDBM.parse_document(
        db.division.insert_document(DivisionDBM(title='ЦСМС').document())
    )

    roadmap1 = RoadmapDBM.parse_document(
        db.roadmap.insert_document(RoadmapDBM(
            title='Путь начинающего',
            tasks=[
                TaskDBM(
                    index=0,
                    type=TaskTypes.auto_test,
                    title='Ознакомиться с сайтом Россмолодёжы',
                    text=(
                        'Сперва вам требуется посетить сайт россмолодёжы, '
                        'который указан в приложние, затем пройти тест'
                    ),
                    is_confirmed_by_hr_int_id=None,
                    coins=5,
                    is_completed=False,
                    is_good=None,
                    week_num=1,
                    day_num=1,
                    attachments=[Attachment(title="Наш сайт", url="https://myrosmol.ru/")],
                    quizzes=[
                        QuizDBM(
                            question='Какого цвета наш логотип ?',
                            answer=None,
                            correct_answer='Фиолетовый'
                        ),
                        QuizDBM(
                            question='Какая почта на сайте Россмолодёжи ?',
                            answer=None,
                            correct_answer='Op@fadm.gov.ru'
                        )
                    ]
                ),
                TaskDBM(
                    index=1,
                    type=TaskTypes.hr_confirmation,
                    title='Подпишите документы',
                    text=(
                        'Требуется придти в офис в 6 отдел и подписать документы по новому трудовому кодексу, '
                        'маршрут можете посмотреть в приложении'
                    ),
                    is_confirmed_by_hr_int_id=None,
                    coins=15,
                    is_completed=False,
                    is_good=None,
                    week_num=1,
                    day_num=2,
                    attachments=[Attachment(title="Маршрут", url="https://yandex.ru/maps/-/CCUGA8AMoC")],
                    quizzes=[]
                ),
                TaskDBM(
                    index=2,
                    type=TaskTypes.feedback,
                    title='Дайте обратную связь о том, как провели данный день',
                    text='Нужно пройти опрос ниже )',
                    is_confirmed_by_hr_int_id=123,
                    coins=15,
                    is_completed=False,
                    is_good=None,
                    week_num=1,
                    day_num=3,
                    attachments=[Attachment(title="Наш сайт", url="https://yandex.ru/maps/-/CCUGA8AMoC")],
                    quizzes=[]
                )
            ],
            created_by_int_id=123
        ).document())
    )

    db.user.insert_document(UserDBM(
        fullname='Илья',
        email='ilyakhakimov03@gmail.com',
        tokens=['123'],
        role=Roles.employee.value,
        coins=5,
        position='HTML/CSS/JS developer',
        birth_date=datetime(year=2003, month=3, day=27),
        telegram='https://t.me/PirateThunder',
        whatsapp=None,
        vk='https://vk.com/ilyakhakimov03',
        roadmap_int_id=roadmap1.int_id,
        division_int_id=division1.int_id,
    ).document())

    db.user.insert_document(UserDBM(
        fullname='Денис',
        email='dbarov3@gmail.com',
        tokens=['123'],
        role=Roles.employee.value,
        coins=20,
        position='Android Kotlin Developer',
        birth_date=datetime(year=2003, month=3, day=27),
        telegram='https://t.me/BrightOS',
        whatsapp=None,
        vk='https://vk.com/brightos',
        roadmap_int_id=roadmap1.int_id,
        division_int_id=division1.int_id
    ).document())

    db.user.insert_document(UserDBM(
        fullname='Арсен',
        email='sabarsenrash@gmail.com',
        tokens=['123'],
        role=Roles.employee.value,
        coins=20,
        position='Python Backend Developer',
        birth_date=datetime(year=2003, month=1, day=17),
        telegram='https://t.me/arpakit',
        whatsapp=None,
        vk='https://vk.com/arpakit',
        roadmap_int_id=roadmap1.int_id,
        division_int_id=division1.int_id
    ).document())

    db.event.insert_document(EventDBM(
        title='Встреча с коллективом',
        desc='Нужно подойти в 7 корпус к 413 кабинету в 13:00 для встречи с командой',
        dt=datetime.now() + timedelta(days=7),
        to_user_int_ids=[0, 1],
        division_int_id=division1.int_id
    ).document())
    db.event.insert_document(EventDBM(
        title='Встреча с HR',
        desc='Нужно подойти в 11 корпус в 111 кабинету в 11:00 для встречи с HR',
        dt=datetime.now() + timedelta(days=9),
        to_user_int_ids=[0, 1],
        division_int_id=division1.int_id
    ).document())


if __name__ == '__main__':
    insert_test_data()
