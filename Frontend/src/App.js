import "./App.css";
import LoginPage from "./Pages/LoginPage";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import React from "react";
import Main from "../src/Components/Main";
import StatusTable from "./Components/StatusTable"
import AdminStatusTable from "./Components/adminStatusTable";
import AuthTokenInput from "../src/Components/authTokenInput.js"
function App() {
  return (
    <React.Fragment>
        <Router>
          <Routes>
            <Route exact path="/" element={<LoginPage />} />
            <Route exact path="/dashboard" element={<StatusTable />} />
            <Route exact path="/home" element={<Main />} />
            <Route exact path="/authTokenInput" element={<AuthTokenInput/>}/>
            <Route exact path="/adminDashboard" element={<AdminStatusTable/>}/>
          </Routes>
        </Router>
    </React.Fragment>
  );
}

export default App;
