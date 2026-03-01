from backend.models.game import DifficultyLevel

BASE_SCORES = {
    DifficultyLevel.easy:   100,
    DifficultyLevel.medium: 200,
    DifficultyLevel.hard:   400,
}

HINT_PENALTY = 25

def calc_score(correct: bool, difficulty: DifficultyLevel, hints_used: int) -> int:
    if not correct:
        return 0
    base = BASE_SCORES[difficulty]
    penalty = hints_used * HINT_PENALTY
    return max(base - penalty, 10)  # minimum 10 so a correct guess is always rewarded