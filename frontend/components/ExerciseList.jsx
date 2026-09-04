import { useEffect, useState } from "react";
import Exercise from "./Exercise";

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
    return (
      <div>
        <h2>Resultado</h2>

        <p>
          Você acertou {result.score * 100}%
        </p>

        {result.results.map((exerciseResult) => (
          <div key={exerciseResult.exercise_id}>
            <p>
              Exercício {exerciseResult.exercise_id}:{" "}
              {exerciseResult.is_correct ? "O" : "X"}
            </p>
          </div>
        ))}
      </div>
    );
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