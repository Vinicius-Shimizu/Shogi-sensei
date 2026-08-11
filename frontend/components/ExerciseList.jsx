import { useEffect, useState } from "react";
import Exercise from "./Exercise";

export default function ExerciseList() {
  const [exercises, setExercises] = useState([]);
  const [currentExercise, setCurrentExercise] = useState(0);
  const [loading, setLoading] = useState(true);

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

  function handleAnswer() {
    setCurrentExercise((current) => current + 1);
  }

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (exercises.length === 0) {
    return <div>Nenhum exercício encontrado.</div>;
  }

  if (currentExercise >= exercises.length) {
    return <div>Parabéns! Você terminou os exercícios.</div>;
  }

  return (
    <Exercise
        key={currentExercise}
        exercise={exercises[currentExercise]}
        onAnswer={handleAnswer}
    />
  );
}