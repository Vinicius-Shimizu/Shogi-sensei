import './App.css'
import Home from '../components/Home'
import LoginPage from '../components/LoginPage';
import SignUpPage from '../components/SignUpPage';
import ExerciseList from '../components/ExerciseList';
import ResultsPage from '../components/ResultsPage';
import { HashRouter, Routes, Route } from "react-router-dom";

function App() {
 return (
    <HashRouter>
        <Routes>
            <Route path="/" element={<Home />}></Route>
            <Route path="/login" element={<LoginPage />}></Route>
            <Route path="/signup" element={<SignUpPage />}></Route>
            <Route path="/exercise-list" element={<ExerciseList />}></Route>
            <Route path="/results" element={<ResultsPage />}></Route>
        </Routes>
    </HashRouter>
 )
}

export default App