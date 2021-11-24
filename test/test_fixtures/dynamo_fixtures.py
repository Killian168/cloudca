from uuid import uuid4


class DynamoDbFixtures:
    @staticmethod
    def get_cognito_dynamo_json():
        return {
            "address": {"S": "killians-amazing-address"},
            "birthdate": {"S": "killians-amazing-birthdate"},
            "email": {"S": "killians-amazing-email"},
            "family_name": {"S": "killians-amazing-family_name"},
            "gender": {"S": "killians-amazing-gender"},
            "given_name": {"S": "killians-amazing-given_name"},
            "locale": {"S": "killians-amazing-locale"},
            "role": {"S": "killians-amazing-role"},
            "preferred_username": {"S": "killians-amazing-preferred_username"},
        }

    @staticmethod
    def get_member_no_role_dynamo_json(member_id=None):
        if member_id is None:
            member_id = str(uuid4())
        return {
            "id": {"S": member_id},
            "details": {"M": DynamoDbFixtures.get_cognito_dynamo_json()},
            "manager": {"NULL": True},
            "officer": {"NULL": True},
            "academy_player": {"NULL": True},
            "player": {"NULL": True},
        }

    @staticmethod
    def get_player_dynamo_json(player_id=None):
        if player_id is None:
            player_id = str(uuid4())
        return {
            "id": {"S": player_id},
            "details": {"M": DynamoDbFixtures.get_cognito_dynamo_json()},
            "manager": {"NULL": True},
            "officer": {"NULL": True},
            "academy_player": {"NULL": True},
            "player": {
                "M": {
                    "achievements": {"L": []},
                    "all_time_appearances": {"N": "0"},
                    "all_time_assists": {"N": "0"},
                    "all_time_goals": {"N": "0"},
                    "positions": {"L": []},
                    "season_appearances": {"N": "0"},
                    "season_assists": {"N": "0"},
                    "season_goals": {"N": "0"},
                }
            },
        }

    @staticmethod
    def get_manager_dynamo_json(manager_id=None):
        if manager_id is None:
            manager_id = str(uuid4())
        return {
            "id": {"S": manager_id},
            "details": {"M": DynamoDbFixtures.get_cognito_dynamo_json()},
            "manager": {
                "M": {
                    "favorite_formation": {"S": "killians-amazing-favorite_formation"},
                    "win_record": {"N": "0"},
                    "loss_record": {"N": "0"},
                    "achievements": {"L": []},
                }
            },
            "officer": {"NULL": True},
            "academy_player": {"NULL": True},
            "player": {"NULL": True},
        }

    @staticmethod
    def get_fixture_dynamodb_json():
        return {
            "home_team": {"S": "killians-amazing-home-team"},
            "away_team": {"S": "killians-amazing-away-team"},
            "competition": {"S": "killians-amazing-competition"},
            "location": {"S": "killians-amazing-location"},
            "kick_off_time": {"S": "killians-amazing-kick-off-time"},
            "meeting_time": {"S": "killians-amazing-meeting-time"},
        }

    @staticmethod
    def get_team_dynamodb_json(team_id=None, players=None, managers=None, fixtures=None):
        if team_id is None:
            team_id = str(uuid4())
        if managers is None:
            managers = []
        if players is None:
            players = []
        if fixtures is None:
            fixtures = [{"M": DynamoDbFixtures.get_fixture_dynamodb_json()}]
        return {
            "id": {"S": team_id},
            "name": {"S": "killians-amazing-team-name"},
            "managers": {"L": [{"S": manager} for manager in managers]},
            "players": {"L": [{"S": player} for player in players]},
            "training_times": {"L": [{"S": "killians-amazing-training_times"}]},
            "fixtures": {"L": fixtures},
        }
