import React from "react";
import "../css/NavBar.css";
import { useNavigate } from "react-router-dom";
import { useSignOut } from "react-auth-kit";

const NavBar = () => {
  const signOut = useSignOut();
  const navigate = useNavigate();
  const logOut = () => {
    try {
      signOut();
      console.log("Cookies deleted successfully");
    } catch (err) {
      console.error("Error deleting cookies", err);
    }
    // navigate("/");
  };
  return (
    <>
      <div className="nav-bar">
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <div className="container-fluid">
            <button
              className="navbar-toggler"
              type="button"
              data-mdb-toggle="collapse"
              data-mdb-target="#navbarSupportedContent"
              aria-controls="navbarSupportedContent"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <i className="fas fa-bars"></i>
            </button>
            <div
              className="collapse navbar-collapse"
              id="navbarSupportedContent"
            >
              <a className="navbar-brand mt-2 mt-lg-0" href="#">
                <img
                  src="https://www.cyberark.com/wp-content/uploads/2022/12/cyberark-logo-v2.svg"
                  height="50"
                  width="220"
                  alt="MDB Logo"
                  loading="lazy"
                />
              </a>
              <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                <li className="nav-item">
                  <a
                    className="nav-link"
                    onClick={()=>{
                      navigate("/dashboard")
                    }}
                  >
                    Dashboard
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" onClick={() => {
                        navigate("/home");
                      }}>
                    Home
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" href="#">
                    Documentation
                  </a>
                </li>
              </ul>
            </div>
            <div className="d-flex align-items-center">
              <a className="nav-link" onClick={logOut}>
                Log Out
              </a>
              &nbsp;&nbsp;&nbsp;
            </div>
          </div>
        </nav>
      </div>
    </>
  );
};

export default NavBar;
