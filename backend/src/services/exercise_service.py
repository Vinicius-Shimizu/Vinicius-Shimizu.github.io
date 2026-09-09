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

        self.modules = ["recon", "checkmate-in-one", "drop"]

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


    def update_modules_probs(self, user_id: int):
        user_status = self.user_status_repo.get_by_id(user_id)
        if not user_status or not user_status.recent_performances:
            return
        
        current_module = user_status.current_module
        performance_totals = {
            module: 0.0 
            for module in user_status.modules_probs
        }
        performance_counts = {
            module:0
            for module in user_status.modules_probs
        }

        
        for performance in user_status.recent_performances:
            for module, score in performance.items():
                performance_totals[module] += score
                performance_counts[module] += 1

        average_performance = {}
        for module in performance_totals:
            if performance_counts[module] > 0:
                average_performance[module] = (
                    performance_totals[module]
                    / performance_counts[module]
                )

        new_probs = dict(user_status.modules_probs)
        
        user_status.module_progress = average_performance.get(current_module, 0)
        for module, score in average_performance.items():
            if user_status.modules_probs[module] == 0: continue
            if score < 0.7: new_probs[module] *= 1.2
            else: new_probs[module] *= 0.75

        if performance_counts[current_module] >= 2 and average_performance.get(current_module, 0) >= 0.8:
            current_index = self.modules.index(current_module)
            if current_index + 1 < len(self.modules):
                next_module = self.modules[current_index + 1]
                user_status.current_module = next_module
                new_probs[next_module] = 0.8
                user_status.module_progress = 0.0

        total = sum(new_probs.values())
        for module in new_probs:
            new_probs[module] /= total

        user_status.modules_probs = new_probs

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

        

        self.update_modules_probs(user_id)
        self.session.commit()

        score = 100*sum(result.is_correct for result in results) / len(results)


        return ExerciseListResult(
            user_id=user_id,
            score=score,
            results=results,
        )