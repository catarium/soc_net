import { BrowserRouter, Route, Routes } from "react-router";
import "./App.css";
import Registration from "./components/Registration/Registration.jsx";
import Login from "./components/Login/Login.jsx"
import AllPosts from "./components/AllPosts/AllPosts.jsx";
import SubPosts from "./components/SubPosts/SubPosts.jsx";
import UserProfile from "./components/UserProfile/UserProfile.jsx";

function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<AllPosts/>}/>
                    <Route path="/all" element={<AllPosts/>}/>
                    <Route path="/subs" element={<SubPosts/>}/>
                    <Route path="/profile/:userId" element={<UserProfile/>}/>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/registration" element={<Registration/>}/>
                </Routes>
            </BrowserRouter>
        </>
    );
}

export default App;
