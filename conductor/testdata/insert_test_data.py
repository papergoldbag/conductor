from datetime import datetime

from conductor.core.misc import db
from conductor.db.models import UserDBM, Roles, DivisionDBM, RoadmapDBM, TaskDBM, TaskTypes


def insert_test_data():
    db.drop()

    division = DivisionDBM.parse_document(db.division.insert_document(DivisionDBM(title='Подразделение 1').document()))

    elena = db.user.insert_document(UserDBM(
        fullname='Елена',
        email='elena@gmail.com',
        tokens=[],
        role=Roles.hr.value,
        coins=0,
        position='HT Manager',
        birth_date=datetime.now(),
        description='1',
        telegram='1',
        whatsapp='1',
        vk='1',
        roadmap_int_id=None,
        division_int_id=division.int_id
    ).document())

    db.roadmap.insert_document(RoadmapDBM(
        title='Roadmap 1',
        tasks=[
            TaskDBM(
                type=TaskTypes.auto_test,
                title='Task 1',
                text='asf',
                is_confirmed_by_hr_int_id=None,
                coins=12,
                is_completed=False,
                attachments={},
                quizzes=[]
            )
        ],
        created_by_int_id=elena['int_id']
    ).document())

    db.user.insert_document(UserDBM(
        fullname='Arsen',
        email='sabarsnrash@gmail.com',
        tokens=[],
        role=Roles.employee.value,
        coins=0,
        position='Python backend dev',
        birth_date=datetime.now(),
        description='ZZZ',
        telegram='asf',
        whatsapp='asf',
        vk='asf',
        roadmap_int_id='asfasf',
        division_int_id=division.int_id
    ).document())


insert_test_data()
