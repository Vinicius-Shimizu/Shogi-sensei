import './App.css'
import Home from '../components/Home'
import LoginPage from '../components/LoginPage';
import ExerciseList from '../components/ExerciseList';
import ResultsPage from '../components/ResultsPage';
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
 return (
    <BrowserRouter basename="/Shogi-sensei/demo">
        <Routes>
            <Route path="/" element={<Home />}></Route>
            <Route path="/login" element={<LoginPage />}></Route>
            <Route path="/exercise-list" element={<ExerciseList />}></Route>
            <Route path="/results" element={<ResultsPage />}></Route>
            
        </Routes>
    </BrowserRouter>
 )
}

export default App