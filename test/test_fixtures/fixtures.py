from uuid import uuid4


class Fixtures:
    @staticmethod
    def get_member_no_role_json(member_id=None):
        if member_id is None:
            member_id = str(uuid4())
        return {
            "id": member_id,
            "details": {
                "address": "killians-amazing-address",
                "birthdate": "killians-amazing-birthdate",
                "email": "killians-amazing-email",
                "family_name": "killians-amazing-family_name",
                "gender": "killians-amazing-gender",
                "given_name": "killians-amazing-given_name",
                "locale": "killians-amazing-locale",
                "middle_name": None,
                "name": None,
                "nick_name": None,
                "phone_number": None,
                "picture": None,
                "preferred_username": "killians-amazing-preferred_username",
                "profile": None,
                "updated_at": None,
            },
            "manager": None,
            "officer": None,
            "academy_player": None,
            "player": None,
        }

    @staticmethod
    def get_manager_json(manager_id=None):
        if manager_id is None:
            manager_id = str(uuid4())
        return {
            "academy_player": None,
            "details": {
                "address": "killians-amazing-address",
                "birthdate": "killians-amazing-birthdate",
                "email": "killians-amazing-email",
                "family_name": "killians-amazing-family_name",
                "gender": "killians-amazing-gender",
                "given_name": "killians-amazing-given_name",
                "locale": "killians-amazing-locale",
                "middle_name": None,
                "name": None,
                "nick_name": None,
                "phone_number": None,
                "picture": None,
                "preferred_username": "killians-amazing-preferred_username",
                "profile": None,
                "updated_at": None,
            },
            "id": manager_id,
            "manager": {
                "achievements": [],
                "favorite_formation": "killians-amazing-favorite_formation",
                "loss_record": 0,
                "win_record": 0,
            },
            "officer": None,
            "player": None,
        }

    @staticmethod
    def get_player_json(player_id=None):
        if player_id is None:
            player_id = str(uuid4())
        return {
            "academy_player": None,
            "details": {
                "address": "killians-amazing-address",
                "birthdate": "killians-amazing-birthdate",
                "email": "killians-amazing-email",
                "family_name": "killians-amazing-family_name",
                "gender": "killians-amazing-gender",
                "given_name": "killians-amazing-given_name",
                "locale": "killians-amazing-locale",
                "middle_name": None,
                "name": None,
                "nick_name": None,
                "phone_number": None,
                "picture": None,
                "preferred_username": "killians-amazing-preferred_username",
                "profile": None,
                "updated_at": None,
            },
            "id": player_id,
            "manager": None,
            "officer": None,
            "player": {
                "achievements": [],
                "all_time_appearances": 0,
                "all_time_assists": 0,
                "all_time_goals": 0,
                "positions": [],
                "season_appearances": 0,
                "season_assists": 0,
                "season_goals": 0,
            },
        }

    @staticmethod
    def get_team_json(team_id):
        return {
            "fixtures": [
                {
                    "away_team": "killians-amazing-away-team",
                    "competition": "killians-amazing-competition",
                    "home_team": "killians-amazing-home-team",
                    "kick_off_time": "killians-amazing-kick-off-time",
                    "location": "killians-amazing-location",
                    "meeting_time": "killians-amazing-meeting-time",
                }
            ],
            "id": team_id,
            "managers": [],
            "name": "killians-amazing-team-name",
            "players": [],
            "training_times": ["killians-amazing-training_times"],
        }
