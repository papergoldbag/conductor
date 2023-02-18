import logging
from datetime import datetime, timedelta

from conductor.core.misc import db
from conductor.db.models import UserDBM, Roles, DivisionDBM, RoadmapDBM, TaskDBM, TaskTypes, QuizDBM, Attachment, \
    EventDBM

log = logging.getLogger(__name__)


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
    division4 = DivisionDBM.parse_document(
        db.division.insert_document(DivisionDBM(title='ЦСМС').document())
    )

    owner = db.user.insert_document(UserDBM(
        fullname='Дмитрий Алексеевич',
        email='dmitry@gmail.com',
        tokens=['6'],
        role=Roles.supervisor,
        coins=0,
        position='Project Manger PART A12',
        birth_date=datetime(year=2003, month=1, day=17),
        telegram=None,
        whatsapp=None,
        vk=None,
        roadmap_int_id=None,
        division_int_id=division1.int_id
    ).document())

    template_roadmap = RoadmapDBM.parse_document(
        db.roadmap.insert_document(RoadmapDBM(
            title='Путь начинающего',
            tasks=[
                TaskDBM(
                    index=0,
                    type=TaskTypes.auto_test,
                    title='Ознакомиться с трудовым договором',
                    text=('''
                        Трудовой договор в Российской Федерации В Российской Федерации по трудовому договору 
                        работник принимает на себя обязанность выполнять работу в рамках служебных обязанностей по 
                        определённой специальности, согласно своей квалификации и (или) должности с подчинением 
                        внутреннему трудовому распорядку, а работодатель обязуется обеспечивать соответствующие условия 
                        труда согласно нормам трудового законодательства, правилам внутреннего трудового распорядка, 
                        коллективного и трудового договора.\n\n

                        Подчинение внутреннему трудовому распорядку является одной из основных характеризующих черт 
                        трудового договора, отделяющих его от различных гражданско-правовых договоров (подряда, 
                        оказания услуг и пр.).\n\n

                        Дополнительными отличиями гражданско-правовых договоров от трудового договора являются: равенство 
                        сторон гражданско-правовых договоров; наличие овеществлённого результата работ по ним либо 
                        конкретный итог предоставления услуг и передача его контрагенту по акту приёма-передачи; 
                        осуществление по гражданско-правовым договорам единовременной оплаты либо по частям, 
                        которые зависят от готовности результата работ либо от частичного оказания услуг, с составлением 
                        актов приёма- передачи (этапов) выполнения работ (оказания услуг).\n\n

                        Служебные обязанности и иные особенности работы на определённой должности регулируются 
                        должностной инструкцией, с которой работника обязаны ознакомить при подписании договора, 
                        если они не были перечислены в трудовом договоре.\n\n

                        Перед заключением трудового договора на работодателе лежит обязанность по ознакомлению работника 
                        также с иными локальными нормативными актами организации.\n\n

                        Обязательные нормы трудового договора в основном регулируются Трудовым кодексом и иными правовыми 
                        актами трудового законодательства, а для отдельных организаций, отраслей хозяйства или 
                        административно-территориальных единиц могут устанавливаться также коллективными договорами.\n\n

                        Действиям работодателя и работника, направленным на приём на работу по определённой 
                        специальности либо должности, присущ следующий алгоритм: ознакомление будущего работника с 
                        правилами внутреннего распорядка, должностной инструкцией и выдача их копий работнику 
                        (по требованию); подписание (заключение) трудового договора; издание 
                        (на основании трудового договора) приказа о принятии работника на работу; 
                        внесение записи (на основании приказа) о приёме на работу в трудовую книжку работника.'''
                          ),
                    is_confirmed_by_hr_int_id=None,
                    coins=5,
                    is_completed=False,
                    is_good=None,
                    week_num=1,
                    day_num=1,
                    attachments=[
                        Attachment(
                            title="ТК РФ Статья 56 (Трудовой кодекс)",
                            url="http://www.consultant.ru/document/cons_doc_LAW_34683"
                                "/1eaf2e1beb877bbca22338c719320a5b9c692297/"
                        ),
                        Attachment(
                            title='Трудовой кодекс IT специалиста',
                            url='https://www.documentoved.ru/documents/special-documents/trudovoi-dogovor-s-IT'
                        )
                    ],
                    quizzes=[
                        QuizDBM(
                            question='Какой номер статьи отвечает за трудовоq договор ?',
                            answer=None,
                            correct_answer='56'
                        ),
                        QuizDBM(
                            question='Какой номер трудового договора отвечает за IT тематику ?',
                            answer=None,
                            correct_answer='455'
                        )
                    ]
                ),
                TaskDBM(
                    index=1,
                    type=TaskTypes.hr_confirmation,
                    title='Подпись документов',
                    text=(
                        'Требуется придти в офис в 6 отдел и подписать документы по новому трудовому кодексу, '
                        'маршрут можете посмотреть по ссылке.'
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
                    title='Дать обратную связь о том, как прошли первые рабочие дни',
                    text=('''
                        Нам очень важно понимать и осознавать ваше состояние после первых рабочих дней
                    '''),
                    is_confirmed_by_hr_int_id=None,
                    coins=20,
                    is_completed=False,
                    is_good=None,
                    week_num=1,
                    day_num=3,
                    attachments=[],
                    quizzes=[
                        QuizDBM(
                            question='Вам нравятся ваши условия ?',
                            answer=None,
                            correct_answer='1'
                        ), QuizDBM(
                            question='Вы бы хотели что-то поменять в отношение к вам ваших сотрудников ?',
                            answer=None,
                            correct_answer='2'
                        ), QuizDBM(
                            question='Что вам больше всего не понравилось на первых днях ?',
                            answer=None,
                            correct_answer='3'
                        )
                    ]
                ),
                TaskDBM(
                    index=3,
                    type=TaskTypes.auto_test,
                    title='Просто пройдите этот тест ))',
                    text='''Просто пройдите данный тест''',
                    is_confirmed_by_hr_int_id=None,
                    coins=20,
                    is_completed=False,
                    is_good=None,
                    week_num=1,
                    day_num=4,
                    attachments=[],
                    quizzes=[
                        QuizDBM(
                            question='1',
                            answer=None,
                            correct_answer='1'
                        ), QuizDBM(
                            question='2',
                            answer=None,
                            correct_answer='2'
                        ), QuizDBM(
                            question='3',
                            answer=None,
                            correct_answer='3'
                        ), QuizDBM(
                            question='4',
                            answer=None,
                            correct_answer='4'
                        ), QuizDBM(
                            question='5',
                            answer=None,
                            correct_answer='5'
                        )
                    ]
                ),
                TaskDBM(
                    index=4,
                    type=TaskTypes.auto_test,
                    title='Просто пройдите этот тест ))',
                    text='''Просто пройдите данный тест''',
                    is_confirmed_by_hr_int_id=None,
                    coins=20,
                    is_completed=False,
                    is_good=None,
                    week_num=1,
                    day_num=5,
                    attachments=[],
                    quizzes=[
                        QuizDBM(
                            question='1',
                            answer=None,
                            correct_answer='1'
                        ), QuizDBM(
                            question='2',
                            answer=None,
                            correct_answer='2'
                        ), QuizDBM(
                            question='3',
                            answer=None,
                            correct_answer='3'
                        ), QuizDBM(
                            question='4',
                            answer=None,
                            correct_answer='4'
                        ), QuizDBM(
                            question='5',
                            answer=None,
                            correct_answer='5'
                        )
                    ]
                ),
                TaskDBM(
                    index=5,
                    type=TaskTypes.auto_test,
                    title='Просто пройдите этот тест ))',
                    text='''Просто пройдите данный тест''',
                    is_confirmed_by_hr_int_id=None,
                    coins=20,
                    is_completed=False,
                    is_good=None,
                    week_num=2,
                    day_num=1,
                    attachments=[],
                    quizzes=[
                        QuizDBM(
                            question='1',
                            answer=None,
                            correct_answer='1'
                        ), QuizDBM(
                            question='2',
                            answer=None,
                            correct_answer='2'
                        ), QuizDBM(
                            question='3',
                            answer=None,
                            correct_answer='3'
                        ), QuizDBM(
                            question='4',
                            answer=None,
                            correct_answer='4'
                        ), QuizDBM(
                            question='5',
                            answer=None,
                            correct_answer='5'
                        )
                    ]
                )
            ],
            created_by_int_id=owner['int_id']
        ).document())
    )

    db.roadmap_template.insert_document(template_roadmap.document())

    roadmap1_doc = template_roadmap.document()
    roadmap1_doc.pop('int_id', None)
    roadmap1_doc.pop('_id', None)
    roadmap1_doc.pop('created', None)

    roadmap2 = RoadmapDBM.parse_document(db.roadmap.insert_document(roadmap1_doc))
    roadmap1_doc.pop('int_id', None)
    roadmap1_doc.pop('_id', None)
    roadmap1_doc.pop('created', None)

    roadmap3 = RoadmapDBM.parse_document(db.roadmap.insert_document(roadmap1_doc))
    roadmap1_doc.pop('int_id', None)
    roadmap1_doc.pop('_id', None)
    roadmap1_doc.pop('created', None)

    roadmap4 = RoadmapDBM.parse_document(db.roadmap.insert_document(roadmap1_doc))
    roadmap1_doc.pop('int_id', None)
    roadmap1_doc.pop('_id', None)
    roadmap1_doc.pop('created', None)

    roadmap5 = RoadmapDBM.parse_document(db.roadmap.insert_document(roadmap1_doc))

    db.user.insert_document(UserDBM(
        fullname='Илья Хакимов',
        email='ilyakhakimov03@gmail.com',
        tokens=['1'],
        role=Roles.employee,
        coins=0,
        position='HTML/CSS/JS developer',
        birth_date=datetime(year=2003, month=3, day=27),
        telegram='https://t.me/PirateThunder',
        whatsapp=None,
        vk='https://vk.com/ilyakhakimov03',
        roadmap_int_id=template_roadmap.int_id,
        division_int_id=division1.int_id,
    ).document())

    db.user.insert_document(UserDBM(
        fullname='Денис',
        email='dbarov3@gmail.com',
        tokens=['2'],
        role=Roles.hr,
        coins=20,
        position='Android Kotlin Developer',
        birth_date=datetime(year=2003, month=3, day=27),
        telegram='https://t.me/BrightOS',
        whatsapp=None,
        vk='https://vk.com/brightos',
        roadmap_int_id=roadmap2.int_id,
        division_int_id=division1.int_id
    ).document())

    db.user.insert_document(UserDBM(
        fullname='Арсен',
        email='sabarsenrash@gmail.com',
        tokens=['3'],
        role=Roles.supervisor,
        coins=20,
        position='Python Backend Developer',
        birth_date=datetime(year=2003, month=1, day=17),
        telegram='https://t.me/arpakit',
        whatsapp=None,
        vk='https://vk.com/arpakit',
        roadmap_int_id=roadmap3.int_id,
        division_int_id=division1.int_id
    ).document())

    db.user.insert_document(UserDBM(
        fullname='Рустам Афанасьев',
        email='rosutamu.afanasev@gmail.com',
        tokens=['4'],
        role=Roles.supervisor,
        coins=20,
        position='Python Backend Developer',
        birth_date=datetime(year=2003, month=1, day=17),
        telegram='https://t.me/arpakit',
        whatsapp=None,
        vk='https://vk.com/arpakit',
        roadmap_int_id=roadmap4.int_id,
        division_int_id=division1.int_id
    ).document())

    db.user.insert_document(UserDBM(
        fullname='Иван Ермолов',
        email='ivan.afanasev@gmail.com',
        tokens=['5'],
        role=Roles.employee,
        coins=20,
        position='Python Backend Developer',
        birth_date=datetime(year=2003, month=1, day=17),
        telegram='https://t.me/arpakit',
        whatsapp=None,
        vk='https://vk.com/arpakit',
        roadmap_int_id=roadmap5.int_id,
        division_int_id=division1.int_id
    ).document())

    db.event.insert_document(EventDBM(
        title='Встреча с коллективом',
        desc='Нужно подойти в 7 корпус к 413 кабинету в 13:00 для встречи с командой',
        dt=datetime.now() + timedelta(days=7),

        division_int_id=division1.int_id
    ).document())
    db.event.insert_document(EventDBM(
        title='Встреча с HR и руководителем',
        desc='Нужно подойти в 11 корпус в 111 кабинету в 11:00 для встречи с HR',
        dt=datetime.now() + timedelta(days=9),
        division_int_id=division1.int_id
    ).document())
    db.event.insert_document(EventDBM(
        title='Coffee brake с командой',
        desc='Встреча будет в кафе у уровня 9',
        dt=datetime.now() + timedelta(days=4),
        division_int_id=division1.int_id
    ).document())

    log.info('test_data were inserted')


if __name__ == '__main__':
    insert_test_data()
