import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import { DialogContent } from "@mui/material";
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import { useNavigate } from "react-router-dom";
const AuthTokenInput = () => {
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
          //   onChange={(e) => {
          //     setIP(e.target.value);
          //   }}
          //   value={IP}
          rows={4}
          cols={10}
        />
      </DialogContent>
      <DialogActions className="dialog-actions">
        <button className="submit-button" onClick={()=>{
            navigate("/adminDashboard")
        }}>
          Submit
        </button>
      </DialogActions>
    </Dialog>
  );
};

export default AuthTokenInput;
