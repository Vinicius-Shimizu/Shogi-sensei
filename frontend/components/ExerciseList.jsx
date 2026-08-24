import { useEffect, useState } from "react";
import Exercise from "./Exercise";

export default function ExerciseList() {
  const [exercises, setExercises] = useState([]);
  const [currentExercise, setCurrentExercise] = useState(0);
  const [loading, setLoading] = useState(true);
  const [correctAnswers, setCorrectAnswers] = useState([]);
  const [progressUpdated, setProgressUpdated] = useState(false);

  useEffect(() => {
    async function fetchExercises() {
      try {
        const response = await fetch(
          "http://localhost:8000/exercises/exercise_list"
        );

        const data = await response.json();

        setExercises(data.response);
      } catch (error) {
        console.error("Erro ao buscar exercícios:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchExercises();
  }, []);

  async function updateUserProgress(score) {
    try {
      const response = await fetch(
        "http://localhost:8000/exercises/update_user_progress",
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            lesson_score: score,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Erro ao atualizar progresso");
      }

      console.log("Progresso atualizado com sucesso");
    } catch (error) {
      console.error("Erro ao atualizar progresso:", error);
    }
  }

  useEffect(() => {
    if (
      exercises.length > 0 &&
      currentExercise >= exercises.length &&
      !progressUpdated
    ) {
      const lessonScore =
        (correctAnswers.length / exercises.length) * 100;

      updateUserProgress(lessonScore);
      setProgressUpdated(true);
    }
  }, [
    currentExercise,
    exercises.length,
    correctAnswers,
    progressUpdated,
  ]);

  function handleAnswer(correct) {
    if (correct) {
      setCorrectAnswers((answers) => [
        ...answers,
        currentExercise,
      ]);
    }

    setCurrentExercise((current) => current + 1);
  }

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (exercises.length === 0) {
    return <div>Nenhum exercício encontrado.</div>;
  }

  if (currentExercise >= exercises.length) {
    const lessonScore =
      (correctAnswers.length / exercises.length) * 100;

    return <div>Você acertou {lessonScore}%</div>;
  }

  return (
    <Exercise
      key={currentExercise}
      exercise={exercises[currentExercise]}
      onAnswer={handleAnswer}
    />
  );
}