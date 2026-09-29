import './App.css'
import ExerciseList from '../components/ExerciseList'
import Home from '../components/Home'
import LoginPage from '../components/LoginPage';
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
 return (
    <BrowserRouter basename="/Shogi-sensei/demo">
        <Routes>
            <Route path="/" element={<Home />}></Route>
            <Route path="/login" element={<LoginPage />}></Route>

        </Routes>
    </BrowserRouter>
 )
}

export default App