import { useEffect, useState, useRef } from "react";
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
  const [submitError, setSubmitError] = useState(false);

  const API_URL=import.meta.env.VITE_BACKEND_API_URL;
  const token = localStorage.getItem("access_token");

  const navigate = useNavigate();

  const exerciseStartTime = useRef(null);

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
    }
  }, [API_URL, token, navigate]);

  useEffect(() => {
    if (exercises.length > 0) {
      exerciseStartTime.current = performance.now();
    }
  }, [currentExercise, exercises]);


  async function submitAnswers(finalAnswers) {
    setSubmitting(true);
    setSubmitError(false);
    
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
            answers: finalAnswers.slice(0, 10),
          }),
        }
      );

      if (response.status === 401) {
        localStorage.removeItem("access_token");
        navigate("/login");
        return;
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        console.error("Erro ao enviar a lista:", errorData);
        setSubmitError(true);
        return;
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
      setSubmitError(true);
    } finally {
      setSubmitting(false);
    }
  }

  function handleAnswer(answer) {
    const exercise = exercises[currentExercise];

    const responseTimeMs = Math.round(
      performance.now() - exerciseStartTime.current
    );

    const newAnswer = {
      exercise_id: exercise.exercise_id,
      answer: answer,
      response_time_ms: responseTimeMs
    };
    console.log(newAnswer);
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
    return <div className="w-full min-h-screen bg-black pt-4">Corrigindo exercícios...</div>;
  }
  if (loadingList) {
    return <div className="w-full min-h-screen bg-black pt-4">Carregando...</div>;
  }

  if (exercises.length === 0) {
    return (
      <div className="w-full min-h-screen bg-black pt-4">
        <div>Nenhum exercício encontrado.</div>
        <button onClick={() => navigate("/")} className="flex-col border-2 bg-slate-600 rounded-xl w-[30%] h-[10%] mt-8">Home</button>
      </div>
    )
  }

  if (submitError) {
    function resetExerciseList() {
      localStorage.removeItem("exercise_list");
      localStorage.removeItem("current_exercise");
      localStorage.removeItem("user_answers");

      setExercises([]);
      setAnswers([]);
      setCurrentExercise(0);
      setSubmitError(false);

      navigate("/exercise-list");
    }

    return (
      <div className="w-full min-h-screen bg-black text-white
                      flex flex-col justify-center items-center pt-4">
        <p className="text-center px-4">
          Erro ao enviar a lista. Você pode tentar novamente
          ou começar outra lista.
        </p>

        <button
          onClick={() => submitAnswers(answers)}
          className="border-2 bg-slate-600 rounded-xl
                    w-[80vw] md:w-[30vw] mt-8 py-2"
        >
          Tentar novamente
        </button>

        <button
          onClick={resetExerciseList}
          className="flex flex-col justify-center items-center
                    border-2 bg-wood text-black rounded-xl
                    w-[80vw] md:w-[30vw] mt-4 py-2"
        >
          Começar outra lista
        </button>
      </div>
    );
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