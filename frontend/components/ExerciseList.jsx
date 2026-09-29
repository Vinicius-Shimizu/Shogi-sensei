import { useEffect, useState } from "react";
import Exercise from "./Exercise";
import { useNavigate } from "react-router-dom";

export default function ExerciseList() {
  const [userId, setUserId] = useState(-1);
  const [exercises, setExercises] = useState([]);
  const [currentExercise, setCurrentExercise] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [loadingUser, setLoadingUser] = useState(true);
  const [loadingList, setLoadingList] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const API_URL=import.meta.env.VITE_BACKEND_API_URL;
  const token = localStorage.getItem("access_token");
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      console.log("Usuário não autenticado");
      navigate("/login");
    }
  }, [token, navigate]);
  
  useEffect(() => {
    async function getUserId() {
      try {
        const response = await fetch(
          `${API_URL}/users/me`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Erro ao buscar usuário");
        }

        const data = await response.json();
        setUserId(data.id);
      } catch (error) {
        console.log(error);
      } finally {
        setLoadingUser(false);
      }
    }

    if (token) {
      getUserId();
    }
  }, [API_URL, token]);
  
  useEffect(() => {
    async function fetchExercises() {
      try {
        const response = await fetch(
          `${API_URL}/exercises/list?user_id=${userId}`
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
        setLoadingList(false);
      }
    }

    if (userId !== -1) {
      fetchExercises();
    }
  }, [userId, API_URL]);

  async function submitAnswers(finalAnswers) {
    setSubmitting(true);

    try {
      const response = await fetch(
        `${API_URL}/exercises/submit`,
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

      navigate("/results", {
        state: { result: data },
      });
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

  if (loadingUser || loadingList) {
    return <div>Carregando...</div>;
  }

  if (exercises.length === 0) {
    return (
      <div className="h-screen">
        <div>Nenhum exercício encontrado.</div>
        <button onClick={() => navigate("/")} className="flex-col border-2 bg-slate-600 rounded-xl w-[30%] h-[10%] mt-8">Home</button>
      </div>
    )
  }

  if (submitting) {
    return <div>Corrigindo exercícios...</div>;
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