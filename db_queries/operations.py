from db_queries.models import User


def get_user(session, user_id):
    user = session.query(User).filter(User.user_id == user_id).one_or_none()
    return user


def upsert_user(session, user_id, user_name, battle_tag):
    # Fetch the existing user
    user = get_user(session, user_id)

    # If the user exists, update as BattleTag or username as necessary
    if user:
        messages = []
        if user_name and user_name != user.user_name:
            user.user_name = user_name
            messages.append(f"Username updated to {user_name}.")
        if battle_tag is not None and battle_tag != user.battle_tag:
            user.battle_tag = battle_tag
            messages.append(f"Battle tag updated to {battle_tag}.")
        elif battle_tag is None:
            messages.append(f"The current battle tag for user ID {user_id} is {user.battle_tag}.")

        # If there were any updates, commit the session
        if messages:
            session.commit()

        # If there were no changes to username or battle_tag
        if not messages:
            messages.append("No updates were made as no changes were detected.")

        return " ".join(messages)

    # If the user doesn't exist and a valid battle tag is provided, add a new user
    elif battle_tag is not None:
        user = User(user_id=user_id, user_name=user_name, battle_tag=battle_tag)
        session.add(user)
        session.commit()
        return f"User ID {user_id} added successfully."

    # If the user doesn't exist and no battle tag is provided, report back
    else:
        return f"No user found with ID {user_id}. No action taken."
