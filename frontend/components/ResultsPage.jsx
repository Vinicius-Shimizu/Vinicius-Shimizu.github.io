import ExerciseList from "./ExerciseList";

export default function ResultsPage({result, onRestart}){
    return (
      <div>
        <h2>Resultado</h2>

        <p>
          Você acertou {result.score}%
        </p>

        {result.results.map((exerciseResult, index) => (
          <div key={exerciseResult.exercise_id}>
            <p>
              Exercício {index + 1}:{" "}
              {exerciseResult.is_correct ? "O" : "X"}
            </p>
          </div>
        ))}
        <button onClick={onRestart}>Tentar de novo</button>
      </div>
    );
}