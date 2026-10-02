import { useEffect, useState } from "react";
import Exercise from "./Exercise";
import { useNavigate } from "react-router-dom";

export default function ExerciseList() {
  const [exercises, setExercises] = useState([]);
    const [currentExercise, setCurrentExercise] = useState(() => {
    const saved = localStorage.getItem("current_exercise");
    return saved ? Number(saved) : 0;
  });
  const [answers, setAnswers] = useState(() => {
    const saved = localStorage.getItem("user_answers");
    return saved ? JSON.parse(saved) : [];
  });
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
    async function fetchExercises() {
      const savedList = localStorage.getItem("exercise_list");

      if (savedList) {
        const savedExercises = JSON.parse(savedList);
        setExercises(savedExercises);
        setLoadingList(false);
        if(savedExercises.length == answers.length){
           submitAnswers(answers);
        }
        return;
      }
      try {
        const response = await fetch(
          `${API_URL}/exercises/list`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        
        if (response.status === 401) {
          localStorage.removeItem("access_token");
          navigate("/login");
          return;
        }
        
        if (!response.ok) {
          throw new Error("Erro ao buscar exercícios");
        }

        const data = await response.json();

        setExercises(data);
        localStorage.setItem("exercise_list", JSON.stringify(data));
      } catch (error) {
        console.error("Erro ao buscar exercícios:", error);
      } finally {
        setLoadingList(false);
      }
    }

    if (token) {
      fetchExercises();
      console.log(exercises);
    }
  }, [API_URL, token, navigate]);

  async function submitAnswers(finalAnswers) {
    setSubmitting(true);

    try {
      const response = await fetch(
        `${API_URL}/exercises/submit`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            answers: finalAnswers,
          }),
        }
      );

      if (response.status === 401) {
        localStorage.removeItem("access_token");
        navigate("/login");
        return;
      }

      if (!response.ok) {
        throw new Error("Erro ao enviar respostas");
      }

      const data = await response.json();
      localStorage.removeItem("exercise_list");
      localStorage.removeItem("current_exercise");
      localStorage.removeItem("user_answers");

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
    localStorage.setItem(
      "user_answers",
      JSON.stringify(newAnswers)
    );
    const nextExercise = currentExercise + 1;
    
    if (nextExercise >= exercises.length) {
      submitAnswers(newAnswers);
      return;
    }

    setCurrentExercise(nextExercise);
    localStorage.setItem(
      "current_exercise",
      nextExercise.toString()
    );
  }
  if (submitting) {
    return <div className="w-full min-h-screen bg-black">Corrigindo exercícios...</div>;
  }
  if (loadingList) {
    return <div className="w-full min-h-screen bg-black">Carregando...</div>;
  }

  if (exercises.length === 0) {
    return (
      <div className="w-full min-h-screen bg-black">
        <div>Nenhum exercício encontrado.</div>
        <button onClick={() => navigate("/")} className="flex-col border-2 bg-slate-600 rounded-xl w-[30%] h-[10%] mt-8">Home</button>
      </div>
    )
  }

  


  return (
    <div className={`w-full min-h-screen bg-black justify-center items-center`}>
      <Exercise
        key={currentExercise}
        exercise={exercises[currentExercise]}
        onAnswer={handleAnswer}
        exerciseNumber={currentExercise}
        totalExercises={exercises.length}
        />
    </div>
  );
}