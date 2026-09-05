from sqlalchemy.orm import Session

from src.database.repositories.raw_games import RawGameRepository
from src.database.repositories.exercise import ExerciseRepository
from src.database.repositories.user_status import UserStatusRepository
from src.exercise_generator import ExerciseGenerator
from src.schemas.exercises import ExerciseAnswer, ExerciseResult, ExerciseListResult

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

    def generate_recon(self):
        batch_processed = False
        games = self.raw_games_repo.get_unprocessed_games()
        if not games:
            batch_processed = True
            games = self.raw_games_repo.get_random(limit=300)
        exercises = self.generator.recon(games)
        print(exercises)
        if exercises:
            self.exercise_repo.bulk_insert(exercises)

        if not batch_processed:
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
        return self.exercise_repo.get_exercises_list(user_status.modules_probs)

    def submit_answers(self, user_id: int, answers: list[ExerciseAnswer]):
        results = []

        for answer in answers:
            exercise = self.exercise_repo.get_by_id(answer.exercise_id)

            if exercise is None:
                continue
            solution = exercise.solution.split(":")[0]
            is_correct = (answer.answer == solution)

            results.append(
                ExerciseResult(
                    exercise_id=exercise.exercise_id,
                    exercise_type=exercise.type,
                    answer=answer.answer,
                    solution=solution,
                    is_correct=is_correct,
                )
            )

        if not results:
            return None

        user_status = self.user_status_repo.get_by_id(user_id)
        if not user_status: return None

        score_per_module = {}
        totals = {}

        for result in results:
            exercise_type = result.exercise_type

            totals[exercise_type] = totals.get(exercise_type, 0) + 1

            if result.is_correct: score_per_module[exercise_type] = score_per_module.get(exercise_type, 0) + 1
            else: score_per_module.setdefault(exercise_type, 0)

        for exercise_type in score_per_module: score_per_module[exercise_type] /= totals[exercise_type]

        user_status.recent_performances = (
            user_status.recent_performances + [score_per_module]
        )[-10:]
        self.session.commit()

        score = 100*sum(result.is_correct for result in results) / len(results)
        return ExerciseListResult(
            user_id=user_id,
            score=score,
            results=results,
        )