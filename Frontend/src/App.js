import "./App.css";
import LoginPage from "./Pages/LoginPage";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import React from "react";
import Main from "../src/Components/Main";
import UserDashboard from "./Components/userDashboard"
import AdminDashboard from "./Components/adminDashboard.js";
import AuthTokenInput from "../src/Components/authTokenInput.js"
import { RequireAuth } from "react-auth-kit";
function App() {
  return (
    <React.Fragment>
        <Router>
          <Routes>
            <Route exact path="/" element={<LoginPage />} />
            <Route exact path="/dashboard" element={<RequireAuth loginPath="/"><UserDashboard /></RequireAuth>} />
            <Route exact path="/home" element={<RequireAuth loginPath="/"><Main /></RequireAuth>} />
            <Route exact path="/authTokenInput" element={<RequireAuth loginPath="/"><AuthTokenInput/></RequireAuth>}/>
            <Route exact path="/adminDashboard" element={<RequireAuth loginPath="/"><AdminDashboard/></RequireAuth>}/>
          </Routes>
        </Router>
    </React.Fragment>
  );
}

export default App;

<RequireAuth loginPath="/"></RequireAuth>
