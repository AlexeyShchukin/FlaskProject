from datetime import datetime

from sqlalchemy import desc, or_, and_, func
from sqlalchemy.orm import aliased

from sqlalchemy_lessons import engine
from sqlalchemy_lessons.db_connector import DBConnector
from sqlalchemy_lessons.social_blogs_models import Role, User, News, Comment


with DBConnector(engine=engine) as session:
    # users = session.query(User)  # SELECT * FROM users

    # print(users)
    # print("=" * 100)

    # for user in users.all():
    #     print(user.email, user.roll_id, user.rating)

    # us = users.first()
    # print(us.email, us.roll_id, us.rating)

    # user = session.query(User).filter(User.rating > 4).one()  # returning one or exception if None or more then one
    # print(user)

    # user = session.query(User).filter(User.rating > 4).one_or_none()  # returning one/None or exception if more then one
    # print(user)

    # moderator_users = session.query(User).filter_by(role_id=2).all()
    # for user in moderator_users:
    #     print(user.last_name, user.role_id, user.role.name)

    # moderator_users = session.query(User).filter(
    #     User.last_name.like('W%')
    # ).all()
    # for user in moderator_users:
    #     print(user.last_name, user.role_id, user.role.name)

    # users = session.query(User).filter(
    #     User.rating.between(5,8)
    # ).all()
    # for user in users:
    #     print(user.last_name, user.rating, user.role.name)

    # req_names = {"Mcneil", "Randolph", "Miller"}
    # users = session.query(User).filter(
    #     User.last_name.in_(req_names)
    # ).all()
    # for user in users:
    #     print(user.last_name, user.rating, user.role.name)

    # users = session.query(User.last_name, User.rating, User.created_at).filter(
    #     or_(
    #         (
    #             and_(
    #                 User.role_id == 3,
    #                 User.rating > 6
    #             )
    #         ),
    #         (User.created_at > datetime.now())
    #     )
    # ).order_by(desc(User.rating)).all()
    # for user in users:
    #     print(user.last_name, user.rating, user.created_at)

    # total_rating = session.query(
    #     User.role_id,
    #     func.avg(User.rating)
    # ).group_by(User.role_id).all()
    #
    # print(total_rating)

    # avg_rating = session.query(func.avg(User.rating)).scalar()  # вернет конкретное значение, а не кортеж
    # print(f'{avg_rating=}')

    # moderated_news_count = session.query(
    #     func.count(News.id)
    # ).filter(News.moderated == 1).scalar()
    #
    # print(f'{moderated_news_count=}')

    # author_news_count = session.query(
    #     News.author_id,
    #     func.count(News.id).label('count_of_news')
    # ).group_by(News.author_id).all()
    #
    # for news in author_news_count:
    #     print(news.author_id, news.count_of_news)

    # us: User = aliased(element=User, name='us')
    #
    # author_news_count = session.query(
    #     us.role_id,
    #     func.count(us.id).label('count_of_users')
    # ).group_by(us.role_id).all()

    us: User = aliased(element=User, name='us')
    us2: User = aliased(element=User, name='us2')

