import "bootstrap/dist/css/bootstrap.min.css";
import { useEffect, useState } from "react";
import IPWhitelist from "./IPWhitelist";
import CertificateUpload from "./CertificateUpload";
import "../css/Main.css";
import React from "react";
import { useNavigate } from "react-router-dom";

function Main() {
  const navigate = useNavigate();
  const [task, setTask] = useState("");
  const [IPWhitelistContentVisible, setIPWhitelistContentVisible] =
    useState(false);
  const [LDAPContentVisible, setLDAPContentVisible] = useState(false);
  const [PSMContentVisible, setPSMContentVisible] = useState(false);
  const [customerId, setCustomerId] = useState("");
  const [open, setOpen] = useState(false);
  const [dropdownVisible, setDropDownVisible] = useState(true);

  useEffect(() => {
    task === "IPWhitelist"
      ? setIPWhitelistContentVisible(true)
      : setIPWhitelistContentVisible(false);
    task === "LDAP"
      ? setLDAPContentVisible(true)
      : setLDAPContentVisible(false);
    task === "PSM" ? setPSMContentVisible(true) : setPSMContentVisible(false);

    if (customerId.length === 0) {
      setDropDownVisible(true);
    } else {
      setDropDownVisible(false);
    }
  }, [task, customerId]);

  const handleOnChange = (e) => {
    setTask(e.target.value);
    handleClickOpen();
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    clearTask();
  };

  const handleSubmit = async (body, type_of_task) => {
    const formData = new FormData();
    formData.set("customer_id", customerId);
    formData.set("type_of_task", type_of_task);
    for (var i = 0; i < body.length; i++) {
      formData.append("body", body[i]);
    }
    formData.set("support_id", "1");
    await fetch("http://localhost:5000/insertIntoDatabase", {
      mode: "cors",
      method: "POST",
      body: formData,
    })
      .then(async (response) => {
        setOpen(false);
        clearTask();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const clearTask = () => {
    document.getElementById("dropdown-basic-button").value = "selectAnOption";
    setTask("");
    setCustomerId("");
  };
  return (
    <React.Fragment>
      <div className="page-body">
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
                <a className="navbar-brand mt-2 mt-lg-0">
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
                      onClick={() => {
                        navigate("/dashboard");
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
                <a
                  className="nav-link"
                  onClick={() => {
                    navigate("/");
                  }}
                >
                  Log Out
                </a>
                &nbsp;&nbsp;&nbsp;
                {/* <div className="dropdown">
                  <ul
                    className="dropdown-menu dropdown-menu-end"
                    aria-labelledby="navbarDropdownMenuLink"
                  >
                    <li>
                      <a className="dropdown-item" href="#">
                        Some news
                      </a>
                    </li>
                    <li>
                      <a className="dropdown-item" href="#">
                        Another news
                      </a>
                    </li>
                    <li>
                      <a className="dropdown-item" href="#">
                        Something else here
                      </a>
                    </li>
                  </ul>
                </div> */}
                {/* <div className="dropdown">
                  <a
                    className="dropdown-toggle d-flex align-items-center hidden-arrow"
                    href="#"
                    id="navbarDropdownMenuAvatar"
                    role="button"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                  >
                    <img
                      src="https://mdbcdn.b-cdn.net/img/new/avatars/2.webp"
                      className="rounded-circle"
                      height="25"
                      alt="Black and White Portrait of a Man"
                      loading="lazy"
                    />
                  </a>
                  <ul
                    className="dropdown-menu dropdown-menu-end"
                    aria-labelledby="navbarDropdownMenuAvatar"
                  >
                    <li>
                      <a className="dropdown-item" href="#">
                        My profile
                      </a>
                    </li>
                    <li>
                      <a className="dropdown-item" href="#">
                        Settings
                      </a>
                    </li>
                    <li>
                      <a className="dropdown-item" href="#">
                        Logout
                      </a>
                    </li>
                  </ul>
                </div> */}
              </div>
            </div>
          </nav>
        </div>
        <div className="main-body">
          <div className="new-request">
            <span>Enter Customer Id :</span>&nbsp;&nbsp;
            <input
              value={customerId}
              className="customer-id"
              type="text"
              style={{ width: "300px" }}
              onChange={(e) => setCustomerId(e.target.value)}
            />
            <br />
            <br />
            <select
              className="form-select"
              id="dropdown-basic-button"
              // value="Select an option"
              onChange={handleOnChange}
              defaultValue="Select an option"
              disabled={dropdownVisible}
            >
              <option
                value="selectAnOption"
                style={{ backgroundColor: "white", color: "black" }}
              >
                Select an option
              </option>
              <option
                value="IPWhitelist"
                style={{ backgroundColor: "white", color: "black" }}
              >
                IP white listing
              </option>
              <option
                value="LDAP"
                style={{ backgroundColor: "white", color: "black" }}
              >
                LDAP certificate upload
              </option>
              <option
                value="PSM"
                style={{ backgroundColor: "white", color: "black" }}
              >
                PSM certificate upload
              </option>
            </select>
            <br />
            <div>{task}</div>
            {IPWhitelistContentVisible && (
              <IPWhitelist
                onSelect={clearTask}
                open={open}
                handleClose={handleClose}
                handleSubmit={handleSubmit}
                customerId={customerId}
              />
            )}
            {LDAPContentVisible && (
              <CertificateUpload
                onSelect={clearTask}
                open={open}
                handleSubmit={handleSubmit}
                handleClose={handleClose}
                customerId={customerId}
                certificateType="LDAP"
                type_of_task={4}
              />
            )}
            {PSMContentVisible && (
              <CertificateUpload
                onSelect={clearTask}
                open={open}
                handleSubmit={handleSubmit}
                handleClose={handleClose}
                customerId={customerId}
                certificateType="PSM"
                type_of_task={3}
              />
            )}
          </div>
          <div className="cards"></div>
        </div>
      </div>
    </React.Fragment>
  );
}

export default Main;
