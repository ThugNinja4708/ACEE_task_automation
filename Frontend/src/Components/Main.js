import "bootstrap/dist/css/bootstrap.min.css";
import { useEffect, useState } from "react";
import IPWhitelist from "./IPWhitelist";
import NavBar from "../Pages/NavBar.js";
import CertificateUpload from "./CertificateUpload";
import "../css/Main.css";
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faExclamationCircle } from "@fortawesome/free-solid-svg-icons";

function Main() {
  const [task, setTask] = useState("");
  const [IPWhitelistContentVisible, setIPWhitelistContentVisible] =
    useState(false);
  const [LDAPContentVisible, setLDAPContentVisible] = useState(false);
  const [PSMContentVisible, setPSMContentVisible] = useState(false);
  const [customerId, setCustomerId] = useState("");
  const [open, setOpen] = useState(false);
  const [dropdownVisible, setDropDownVisible] = useState(true);
  const [validationMessage, setValidationMessage] = useState(
    "Enter valid Customer ID"
  );

  useEffect(() => {
    task === "IPWhitelist"
      ? setIPWhitelistContentVisible(true)
      : setIPWhitelistContentVisible(false);
    task === "LDAP"
      ? setLDAPContentVisible(true)
      : setLDAPContentVisible(false);
    task === "PSM" ? setPSMContentVisible(true) : setPSMContentVisible(false);

    if (customerId.length === 36 && validationMessage.length === 0) {
      setDropDownVisible(false);
    } else {
      setDropDownVisible(true);
    }
  }, [task, customerId, validationMessage]);

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
      .then(async () => {
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

  const customerIDValidation = (event) => {
    const regex = /^[a-f0-9-]+$/;
    setCustomerId(event.target.value);
    if (regex.test(customerId)) {
      if (customerId.length < 36) {
        setValidationMessage("Customer ID must be 36 characters.");
      } else {
        setValidationMessage("");
      }
    } else {
      setValidationMessage("Enter valid Customer ID");
    }
  };
  return (
    <React.Fragment>
      <div className="page-body">
        <NavBar />
        <div className="main-body">
          <div className="new-request">
            <span>Enter Customer Id :</span>&nbsp;&nbsp;
            <input
              value={customerId}
              className="customer-id"
              type="text"
              style={{ width: "300px" }}
              onChange={(event) => {
                setCustomerId(event.target.value);
              }}
              // onKeyUp={customerIDValidation}
            />
            {dropdownVisible && (
              <div className="errorMessage">
                <FontAwesomeIcon icon={faExclamationCircle} className="icon" />
                <p>{validationMessage}</p>
              </div>
            )}
            {!dropdownVisible && (
              <>
                <br />
                <br />
              </>
            )}
            <select
              className="form-select"
              id="dropdown-basic-button"
              onChange={handleOnChange}
              defaultValue="Select an option"
              disabled={!dropdownVisible}
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
