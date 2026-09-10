import { useEffect, useState } from "react";
import Exercise from "./Exercise";
import ResultsPage from "./ResultsPage";


export default function ExerciseList() {
  const [exercises, setExercises] = useState([]);
  const [currentExercise, setCurrentExercise] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const userId = 1;

  useEffect(() => {
    async function fetchExercises() {
      try {
        const response = await fetch(
          `http://localhost:8000/exercises/list?user_id=${userId}`
        );

        if (!response.ok) {
          throw new Error("Erro ao buscar exercícios");
        }

        const data = await response.json();
        console.log(data);
        setExercises(data);
      } catch (error) {
        console.error("Erro ao buscar exercícios:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchExercises();
  }, []);

  async function submitAnswers(finalAnswers) {
    setSubmitting(true);

    try {
      const response = await fetch(
        "http://localhost:8000/exercises/submit",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: userId,
            answers: finalAnswers,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Erro ao enviar respostas");
      }

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.error("Erro ao enviar respostas:", error);
    } finally {
      setSubmitting(false);
    }
  }

  function handleRestart(){
    setCurrentExercise(0);
    setAnswers([]);
    setResult(null);
  }

  function handleAnswer(answer) {
    const exercise = exercises[currentExercise];

    const newAnswer = {
      exercise_id: exercise.exercise_id,
      answer: answer,
    };

    const newAnswers = [...answers, newAnswer];

    setAnswers(newAnswers);

    const nextExercise = currentExercise + 1;

    setCurrentExercise(nextExercise);

    if (nextExercise >= exercises.length) {
      submitAnswers(newAnswers);
    }
  }

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (exercises.length === 0) {
    return <div>Nenhum exercício encontrado.</div>;
  }

  if (submitting) {
    return <div>Corrigindo exercícios...</div>;
  }

  if (result) {
    return <ResultsPage result={result} onRestart={handleRestart}/>
  }

  return (
    <Exercise
      key={currentExercise}
      exercise={exercises[currentExercise]}
      onAnswer={handleAnswer}
      exerciseNumber={currentExercise}
      totalExercises={exercises.length}
      />
  );
}