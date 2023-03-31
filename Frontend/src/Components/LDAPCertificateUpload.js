import { useRef, useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import "../css/LDAPCertificateUpload.css";
import { DialogContent } from "@mui/material";
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";

const LDAPCertificateUpload = (props) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const fileInput = useRef(null);

  const handleFileChange = (event) => {
    setSelectedFiles([...selectedFiles, ...event.target.files]);
  };

  const fileDelete = (name) => {
    const newList = selectedFiles.filter((file) => (
      file.name !== name
    ))
    setSelectedFiles(newList);
  }
  return (
    <>
      <Dialog
        className="ldap-certificate-content"
        open={true}
        keepMounted
        onClose={props.handleClose}
        PaperProps={{
          style: {
            minHeight: "350px",
            borderRadius: "15px",
            textAlign: "center",
            maxHeight: "500px",
          },
        }}
        aria-describedby="alert-dialog-slide-description"
      >
        <DialogContent
          style={{
            width: "600px",
            padding: "0",
          }}
        >
          <div
            className="ldap-header"
          >
            <p className="description"
              // style={{
              //   fontFamily: "Open Sans",
              //   fontSize: "20px",
              //   fontWeight: "600",
              //   borderBottom: "1px solid",
              //   paddingBottom: "6px",
              // }}
            >
              Upload LDAP Certificates
            </p>
          </div>
          <label htmlFor="input-file" className="file-upload-button">
            Choose Certificates
          </label>
          <input
            type="file"
            ref={fileInput}
            id="input-file"
            multiple=".cer,.crt,.pem,.der"
            style={{ display: "none" }}
            onChange={handleFileChange}
          ></input>
          <br />
          <br />
          <ol style={{ paddingLeft: "3rem"}}>
            {selectedFiles.map((file) => (
              <>
              
                <li className="ldap-item" style={{ listStyleType: "none"}}>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="#6a9bca"
                    className="bi bi-x-circle-fill remove-ip-button"
                    viewBox="0 0 16 16"
                    style={{ cursor: "pointer" }}
                    onClick={() => fileDelete(file.name)}
                  >
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z" />
                  </svg>
                  {file.name} 
                </li>
              </>
            ))}
          </ol>
        </DialogContent>
        <DialogActions
          className="dialog-actions"
        >
          <button className="cancel-button" onClick={props.handleClose}>
            Cancel
          </button>
          <button className="submit-button" onClick={props.handleClose}>
            Submit
          </button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default LDAPCertificateUpload;
