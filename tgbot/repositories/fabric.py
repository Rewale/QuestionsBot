from unittest.mock import AsyncMock

from motor.motor_asyncio import AsyncIOMotorClient

from tgbot.repositories import MessagesRepo, Repo, QuestionRepo
from tgbot.repositories.mongo import MessagesMongoRepo, UserMongoRepo, MarkMongoRepo, QuestionMongoRepo
from tgbot.repositories.other import ADUserInfo, SSOJobTitleRoleRepo, fake


def create_repo_ad_sos_pg(mongo_db, ad_url: str, sos_url: str):
    """
    Данные об информации о пользователе и должности берутся из сторонних источников (SOS, AD)
    Остальное содержится в mongodb
    @param mongo_db: база данных
    @param ad_url: адрес АД
    @param sos_url: адрес sos.dom.ru
    @return:
    """
    return Repo(
        message_repo=MessagesMongoRepo(mongo_db),
        question_repo=QuestionMongoRepo(mongo_db),
        user_repo=UserMongoRepo(mongo_db),
        user_info_repo=ADUserInfo(ad_url),
        job_title=SSOJobTitleRoleRepo(sos_url),
        mark_repo=MarkMongoRepo(mongo_db)
    )


def create_repo_mock_services(mongo_db):
    """
    Данные об информации о пользователе и должности МОКУЮТСЯ (SOS, AD)
    Остальное содержится в mongodb
    @param mongo_db: база данных
    @return:
    """
    return Repo(
        message_repo=MessagesMongoRepo(mongo_db),
        question_repo=QuestionMongoRepo(mongo_db),
        user_repo=UserMongoRepo(mongo_db),
        user_info_repo=fake.ADUserInfoFake(),
        job_title=fake.SSOJobTitleRoleRepoFake(),
        mark_repo=MarkMongoRepo(mongo_db)
    )
