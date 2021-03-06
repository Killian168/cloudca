from base64 import b64encode
from pathlib import Path
from uuid import uuid4


class Fixtures:
    test_root = Path(__file__).parents[1]

    @staticmethod
    def get_member_details_json():
        return {
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
        }

    @staticmethod
    def get_member_no_role_json(member_id=None):
        if member_id is None:
            member_id = str(uuid4())
        return {
            "id": member_id,
            "details": Fixtures.get_member_details_json(),
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
            "details": Fixtures.get_member_details_json(),
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
    def get_player_json(player_id=None, season_appearances=0):
        if player_id is None:
            player_id = str(uuid4())
        return {
            "id": player_id,
            "details": Fixtures.get_member_details_json(),
            "manager": None,
            "officer": None,
            "academy_player": None,
            "player": {
                "positions": [],
                "season_appearances": season_appearances,
                "season_assists": 0,
                "season_goals": 0,
                "all_time_appearances": 0,
                "all_time_assists": 0,
                "all_time_goals": 0,
                "achievements": [],
            },
        }

    @staticmethod
    def get_team_no_id_json():
        return {
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
    def get_team_json(team_id=None, team_name=None):
        if team_id is None:
            team_id = str(uuid4())
        if team_name is None:
            team_name = "killians-amazing-team-name"
        return {
            "id": team_id,
            "name": team_name,
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
    def get_base64_sample_pic(image_name=None):
        if image_name is None:
            image_name = "test_image.jpeg"
        image_path = Fixtures.test_root / "resources" / f"{image_name}"
        image = image_path.read_bytes()
        return str(b64encode(image))

    @staticmethod
    def get_dynamo_entry_news_story_json(story_id, thumbnail_key):
        return {
            "id": story_id,
            "category": ["killians-cool-category"],
            "title": "killians-terrible-title",
            "description": "killians-different-description",
            "thumbnail_key": thumbnail_key,
        }

    @staticmethod
    def get_news_story_json(story_id):
        return {
            "id": story_id,
            "category": ["killians-cool-category"],
            "title": "killians-terrible-title",
            "description": "killians-deceptive-description",
            "thumbnail": Fixtures.get_base64_sample_pic(),
        }

    @staticmethod
    def get_s3_object_json(bucket, key):
        return {"bucket": bucket, "key": key}

    @staticmethod
    def get_member_no_id():
        return {
            "details": Fixtures.get_member_details_json(),
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
