from typing import NoReturn

from tutor_site import db_model
from tutor_site.database import Goal, Tutor
from tutor_site.raw_data import teachers


def init_data() -> NoReturn:
    goals = {goal: Goal(goal=goal)
             for teacher in teachers for goal in teacher['goals']}

    db_model.session.add_all(list(goals.values()))

    for teacher in teachers:
        tutor = Tutor(name=teacher['name'],
                      about=teacher['about'],
                      rating=teacher['rating'],
                      picture_url=teacher['picture'],
                      price=teacher['price'],
                      free=teacher['free'],
                      )

        for goal_key, goal in goals.items():
            if goal_key in teacher['goals']:
                tutor.goals.append(goal)

        db_model.session.add(tutor)

    db_model.session.commit()


if __name__ == '__main__':
    init_data()
