from base64 import b64encode
from pathlib import Path
from uuid import uuid4


class Fixtures:
    test_root = Path(__file__).parents[1]

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
            "id": manager_id,
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
            "manager": {
                "favorite_formation": "killians-amazing-favorite_formation",
                "win_record": 0,
                "loss_record": 0,
                "achievements": [],
            },
            "officer": None,
            "academy_player": None,
            "player": None,
        }

    @staticmethod
    def get_player_json(player_id=None):
        if player_id is None:
            player_id = str(uuid4())
        return {
            "id": player_id,
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
            "player": {
                "positions": [],
                "season_appearances": 0,
                "season_assists": 0,
                "season_goals": 0,
                "all_time_appearances": 0,
                "all_time_assists": 0,
                "all_time_goals": 0,
                "achievements": [],
            },
        }

    @staticmethod
    def get_team_json(team_id):
        return {
            "id": team_id,
            "name": "killians-amazing-team-name",
            "managers": [],
            "players": [],
            "training_times": ["killians-amazing-training_times"],
            "fixtures": [
                {
                    "home_team": "killians-amazing-home-team",
                    "away_team": "killians-amazing-away-team",
                    "competition": "killians-amazing-competition",
                    "location": "killians-amazing-location",
                    "kick_off_time": "killians-amazing-kick-off-time",
                    "meeting_time": "killians-amazing-meeting-time",
                }
            ],
        }

    @staticmethod
    def get_base64_sample_pic():
        image_path = Fixtures.test_root / "resources" / "test_image.jpeg"
        image = image_path.read_bytes()
        return b64encode(image)

    @staticmethod
    def get_news_story_json(story_id):
        return {
            "id": story_id,
            "category": ["killians-cool-category"],
            "title": "killians-terrible-title",
            "description": "killians-deceptive-description",
            "thumbnail": Fixtures.get_base64_sample_pic().decode("utf-8"),
        }

    @staticmethod
    def get_s3_object_json(bucket, key):
        return {"bucket": bucket, "key": key}
