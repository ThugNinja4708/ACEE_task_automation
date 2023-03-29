import { useEffect, useRef, useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import "../css/CertificateUpload.css";
import { DialogContent } from "@mui/material";
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";

const CertificateUpload = (props) => {
  const [submitButtonDisabled, setSubmitButtonDisabled] = useState(true);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const fileInput = useRef(null);

  useEffect(() => {
    if (selectedFiles.length === 0 || isLoading) {
      setSubmitButtonDisabled(true);
    } else {
      setSubmitButtonDisabled(false);
    }
  }, [selectedFiles,isLoading]);
  const handleFileChange = (event) => {
    setSelectedFiles([...selectedFiles, ...event.target.files]);
  };

  const fileDelete = (name) => {
    const newList = selectedFiles.filter((file) => file.name !== name);
    setSelectedFiles(newList);
  };
  return (
    <>
      <Dialog
        open={props.open}
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
          <div className="header">
            <p className="description">
              Upload {props.certificateType} Certificates
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
          <ol style={{ paddingLeft: "3rem" }}>
            {selectedFiles.map((file,index) => (
              <>
                <li key={index} className="list-item" style={{ listStyleType: "none" }}>
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
        <DialogActions className="dialog-actions">
          <button className="cancel-button" onClick={props.handleClose}>
            Cancel
          </button>
          <button
            className="submit-button"
            onClick={() => {
              props.handleSubmit(selectedFiles,props.type_of_task);
              setIsLoading(true);
            }}
            disabled={submitButtonDisabled}
          >
            Submit
          </button>
          {isLoading && (
            <>&nbsp;&nbsp;
              <svg
                width="24"
                height="25"
                viewBox="0 0 24 25"
                fill="currentColor"
                xmlns="http://www.w3.org/2000/svg"
                className="pi-spin rotating"
              >
                <path
                  fillRule="evenodd"
                  clipRule="evenodd"
                  d="M10.7061 3.51363C10.7061 2.73396 11.3409 2.09949 12.121 2.09949C12.9011 2.09949 13.5359 2.73396 13.5359 3.51363C13.5359 4.2933 12.9011 4.92777 12.121 4.92777C11.3409 4.92777 10.7061 4.2933 10.7061 3.51363ZM16.2141 5.91262C16.2141 5.01931 16.9373 4.29646 17.8311 4.29646C18.7249 4.29646 19.4481 5.01931 19.4481 5.91262C19.4481 6.80593 18.7249 7.52878 17.8311 7.52878C16.9373 7.52878 16.2141 6.80593 16.2141 5.91262ZM6.4109 4.64999C5.74136 4.64999 5.19814 5.19292 5.19814 5.86211C5.19814 6.53131 5.74136 7.07423 6.4109 7.07423C7.08045 7.07423 7.62367 6.53131 7.62367 5.86211C7.62367 5.19292 7.08045 4.64999 6.4109 4.64999ZM18.3617 11.6197C18.3617 10.6159 19.1765 9.80151 20.1809 9.80151C21.1852 9.80151 22 10.6159 22 11.6197C22 12.6235 21.1852 13.4379 20.1809 13.4379C19.1765 13.4379 18.3617 12.6235 18.3617 11.6197ZM4.01064 10.5591C3.45163 10.5591 3 11.0105 3 11.5692C3 12.1279 3.45163 12.5793 4.01064 12.5793C4.56965 12.5793 5.02128 12.1279 5.02128 11.5692C5.02128 11.0105 4.56965 10.5591 4.01064 10.5591ZM15.7593 17.3268C15.7593 16.2125 16.6657 15.3066 17.7806 15.3066C18.8954 15.3066 19.8019 16.2125 19.8019 17.3268C19.8019 18.441 18.8954 19.347 17.7806 19.347C16.6657 19.347 15.7593 18.441 15.7593 17.3268ZM6.36037 16.4682C5.91506 16.4682 5.55186 16.8312 5.55186 17.2763C5.55186 17.7213 5.91506 18.0843 6.36037 18.0843C6.80568 18.0843 7.16888 17.7213 7.16888 17.2763C7.16888 16.8312 6.80568 16.4682 6.36037 16.4682ZM9.64495 19.6752C9.64495 18.3369 10.7314 17.251 12.0705 17.251C13.4096 17.251 14.496 18.3369 14.496 19.6752C14.496 21.0136 13.4096 22.0995 12.0705 22.0995C10.7314 22.0995 9.64495 21.0136 9.64495 19.6752Z"
                ></path>
              </svg>
              <span>In Progress</span>
            </>
          )}
        </DialogActions>
      </Dialog>
    </>
  );
};

export default CertificateUpload;
