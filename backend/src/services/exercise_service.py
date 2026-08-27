from sqlalchemy.orm import Session

from src.database.repositories.raw_games import RawGameRepository
from src.database.repositories.exercise import ExerciseRepository
from src.database.repositories.user_status import UserStatusRepository
from src.exercise_generator import ExerciseGenerator


class ExerciseService:

    def __init__(self, session: Session):
        self.session = session

        self.raw_games_repo = RawGameRepository(session)
        self.exercise_repo = ExerciseRepository(session)
        self.user_status_repo = UserStatusRepository(session)
        self.generator = ExerciseGenerator(
            "/yaneuraou/yaneuraou"
        )


    def fetch_games(self):
        games = []
        for game in self.generator.get_games():
            parsed_game = self.generator.parse_game(game)
            games.append(parsed_game)

        if not games:
            return 0

        self.raw_games_repo.bulk_insert(games)
        self.session.commit()
        return len(games)


    def generate_checkmate_in_one(self):
        games = self.raw_games_repo.get_unprocessed_games()

        if not games:
            return []
        exercises = self.generator.checkmate_in_one(games)

        if exercises:
            self.exercise_repo.bulk_insert(exercises)

        processed_ids = [
            game.game_id
            for game in games
        ]

        self.raw_games_repo.update_processed(processed_ids)

        self.session.commit()

        return exercises

    def get_exercise_by_id(self, exercise_id: int):
        return self.exercise_repo.get_by_id(exercise_id)

    def get_random_exercise(self):
        return self.exercise_repo.get_random()

    def get_exercise_list(self, user_id: int):
        user_status = self.user_status_repo.get_by_id(user_id)

        if not user_status:
            return None
        print(user_status)
        return self.exercise_repo.get_exercises_list(user_status.modules_probs)