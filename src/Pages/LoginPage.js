import React from "react";
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "../css/LoginPage.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const navigate = useNavigate();
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const handleSubmit = () =>{
    if (userName === "saiteja" && password === "1234") {
      navigate("/home");
    }
    else if(userName === "admin" && password === "admin"){
      navigate("/authTokenInput");
    }
  }
  return (
    <React.Fragment>
      <div className="page">
        <div className="cover">
          <div className="content" style={{ padding: "10%" }}>
            <h3
              style={{
                fontWeight: "500",
                fontFamily: "Fira Sans",
                paddingLeft: "130px",
              }}
            >
              Sign In
            </h3>
            <div
              className="mb-3"
              style={{
                fontFamily: "Fira Sans",
                fontWeight: "500",
                fontSize: "18px",
                paddingTop: "25px",
              }}
            >
              Enter Username
            </div>
            <input
            className="user-credentials"
              type="text"
              placeholder="Enter Username"
              style={{ width: "24em" }}
              onChange={(e) => setUserName(e.target.value)}
            />
            <div
              className="mb-3"
              style={{
                fontFamily: "Fira Sans",
                fontWeight: "500",
                fontSize: "18px",
                paddingTop: "15px",
              }}
            >
               Enter Password
            </div>
            <input
            className="user-credentials"
              type="password"
              placeholder="Enter Password"
              style={{ width: "24em" }}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div
              className="login-btn"
              style={{
                paddingTop: "30px",
                fontSize: "20px",
                width: "100%",
              }}
            >
              <button
                type="submit"
                className="btn btn-primary"
                style={{ width: "360px" }}
                onClick={handleSubmit}
              >
                 Sign In
              </button>
            </div>
          </div>
        </div>
      </div>
    </React.Fragment>
  );
};
export default LoginPage;
