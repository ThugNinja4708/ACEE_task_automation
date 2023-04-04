import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import { DialogContent } from "@mui/material";
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
const AuthTokenInput = () => {
  const [authToken, setAuthToken] = useState("");
  const handleSubmitAuthToken = () => {
  };
  const navigate = useNavigate();
  return (
    <Dialog
      className="ipwhitelist-content"
      open={true}
      keepMounted
      PaperProps={{
        style: {
          minHeight: "320px",
          borderRadius: "15px",
          textAlign: "center",
          maxHeight: "500px",
        },
      }}
      aria-describedby="alert-dialog-slide-description"
    >
      <DialogContent
        style={{
          width: "480px",
          padding: "0",
        }}
      >
        <div className="header">
          <p className="description">Enter Auth Token</p>
        </div>
        <textarea
          className="ip-input auth-input"
          type="text"
          value={authToken}
          onChange={(event) => {
            setAuthToken(event.target.value);
          }}
          rows={4}
          cols={10}
        />
      </DialogContent>
      <DialogActions className="dialog-actions">
        <button className="submit-button" onClick={handleSubmitAuthToken}>
          Submit
        </button>
      </DialogActions>
    </Dialog>
  );
};

export default AuthTokenInput;
