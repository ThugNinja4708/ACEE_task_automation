import { useState } from "react";
import "../css/userDashboard.css";
import "../css/adminDashboard.css";
import data from "../Mock data/data";
import { useEffect } from "react";
import { FaArrowUp, FaArrowDown } from "react-icons/fa";

const AdminDashboard = () => {
  const [users, setUsers] = useState(data);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [searchPhrase, setSearchPhrase] = useState("");
  const [sortOrder, setSortOrder] = useState({ col: "", order: "asc" });
  const formData = new FormData();
  const [tableRefresh, setTableRefresh] = useState(null);
  const taskMapToServiceRequest = {
    1: "IP Whitelist (Add)",
    2: "IP Whitelist (Remove)",
    3: "PSM Certificate Upload",
    4: "LDAP Certificate Upload",
  };

  useEffect(() => {
    const matchedUsers = users.filter((user) => {
      return (
        taskMapToServiceRequest[user.task]
          .toLowerCase()
          .includes(searchPhrase.toLowerCase()) ||
        user.status.toLowerCase().includes(searchPhrase.toLowerCase()) ||
        user.customer_id.toLowerCase().includes(searchPhrase.toLowerCase())
      );
    });
    setFilteredUsers(matchedUsers);
  }, [searchPhrase, tableRefresh]);
  formData.set("support_id", 1);
  useEffect(() => {
    async function fetchData() {
      await fetch("http://localhost:5000//getRequests", {
        mode: "cors",
        method: "POST",
        body: formData,
      }).then(async (response) => {
        const userList = await response.json();
        setUsers(userList);
        setFilteredUsers(userList);
      });
    }
    fetchData();
  }, []);

  const handleApprove = (task_id) => {
    const formData = new FormData();
    formData.set("task_id", [parseInt(task_id)]);
    async function approveTask() {
      await fetch("http://localhost:5000/approveRequest", {
        mode: "cors",
        method: "POST",
        body: formData,
      });
    }
    approveTask();
    setTableRefresh(true);
  };

  const handleRefresh = () => {
    const formData = new FormData();
    formData.set("support_id", 1);
    async function refreshTasks() {
      await fetch("http://localhost:5000/updateTheStatusOfTasks", {
        mode: "cors",
        method: "POST",
        body: formData,
      });
    }
    refreshTasks();
    window.location.reload(false);
  };

  const renderUsers = () => {
    return filteredUsers.map((user, index) => {
      var create_date = user.create_date;
      var year = create_date.substring(0, 4);
      var month = create_date.substring(5, 7);
      var day = create_date.substring(8, 10);
      var created_date = day + "/" + month + "/" + year;
      if (user.complete_date !== null) {
        var complete_date = user.complete_date;
        year = complete_date.substring(0, 4);
        month = complete_date.substring(5, 7);
        day = complete_date.substring(8, 10);
        var completed_date = day + "/" + month + "/" + year;
      } else {
        completed_date = "None";
      }
      const handleShowStatus = (ind) => {
        document
          .getElementById(`approve-button${ind}`)
          .setAttribute("disabled", false);
      };

      return (
        <tr>
          <td className="cid">{user.customer_id}</td>
          {(user.task === 1 && (
            <td className="service-request">IP Whitelist (Add)</td>
          )) ||
            (user.task === 2 && (
              <td className="service-request">IP Whitelist (Remove)</td>
            )) ||
            (user.task === 3 && (
              <td className="service-request">PSM Certificate Upload</td>
            )) ||
            (user.task === 4 && (
              <td className="service-request">LDAP Certificate Upload</td>
            ))}
          <td className="status" id={"approval" + index}>
            {user.status}
          </td>
          {/* <td className="status">{user.Status}</td> */}
          {/* {
            (user.Status == "SUCCESS") && <td className="status" style={{color:"green"}}>{user.Status}</td> ||
            (user.Status == "FAILED") && <td className="status" style={{color:"red"}}>{user.Status}</td> ||
            (user.Status == "IN_PROGRESS") && <td className="status" style={{color:"#e66b19"}}>{user.Status}</td> ||
            (user.Status == "WAITING_FOR_APPROVAL") && <td className="status" style={{color:"#f5b800"}}>{user.Status}</td> ||
            (user.Status == "DENIED") && <td className="status" style={{color:"grey"}}>{user.Status}</td>
          } */}
          <td className="created-date">{created_date}</td>
          <td className="end-date">{completed_date}</td>
          <td style={{ alignContent: "center" }}>
            <button
              className="approve"
              id={"approve-button" + index}
              onClick={(event) => {
                handleApprove(user.task_id);
                handleShowStatus(index);
              }}
              disabled={user.status === "WAITING_FOR_APPROVAL" ? false : true}
            >
              Approve
            </button>
          </td>
          {/* <td id={"approve-status"+index} style={{display:"none"}}>Approved</td> */}
        </tr>
      );
    });
  };

  const sortData = (column) => {
    if (sortOrder.order === "asc") {
      if (column === "service_request") {
        const sortedData = [...data].sort((a, b) => {
          return taskMapToServiceRequest[a["task"]].toLowerCase() >
            taskMapToServiceRequest[b["task"]].toLowerCase()
            ? 1
            : -1;
        });
        setFilteredUsers(sortedData);
      } else if (column === "create_date" || column === "complete_date") {
        const sortedData = [...data].sort(
          (a, b) => new Date(b[column]) - new Date(a[column])
        );
        setFilteredUsers(sortedData);
      } else {
        const sortedData = [...data].sort((a, b) =>
          a[column].toLowerCase() > b[column].toLowerCase() ? 1 : -1
        );
        setFilteredUsers(sortedData);
      }
      setSortOrder({ col: column, order: "desc" });
    }
    if (sortOrder.order === "desc") {
      if (column === "service_request") {
        const sortedData = [...data].sort((a, b) => {
          return taskMapToServiceRequest[b["task"]].toLowerCase() >
            taskMapToServiceRequest[a["task"]].toLowerCase()
            ? 1
            : -1;
        });
        setFilteredUsers(sortedData);
      } else if (column === "create_date" || column === "complete_date") {
        const sortedData = [...data].sort(
          (a, b) => new Date(a[column]) - new Date(b[column])
        );
        setFilteredUsers(sortedData);
      } else {
        const sortedData = [...data].sort((a, b) =>
          a[column].toLowerCase() < b[column].toLowerCase() ? 1 : -1
        );
        setFilteredUsers(sortedData);
      }
      setSortOrder({ col: column, order: "asc" });
    }
  };

  const renderArrow = (column) => {
    if (sortOrder.order === "asc" && sortOrder.col === column) {
      return <FaArrowUp />;
    } else if (sortOrder.order === "desc" && sortOrder.col === column) {
      return <FaArrowDown />;
    } else {
      return null;
    }
  };

  return (
    <>
      <div className="container">
        <div className="table-container" style={{ width: "98%" }}>
          <div className="search-container">
            <p className="status-table-heading">Service Requests Report</p>
            <input
              className="search-input"
              type="text"
              placeholder="Search"
              value={searchPhrase}
              onChange={(event) => {
                setSearchPhrase(event.target.value);
              }}
            />
          </div>
          <table className="status-table">
            <thead>
              <tr>
                <th className="cid">Customer ID</th>
                <th
                  className="service-request"
                  onClick={() => sortData("service_request")}
                >
                  <span style={{ marginRight: 10 }}>Service Request</span>
                  {sortOrder.col === "service_request"
                    ? renderArrow("service_request")
                    : null}
                </th>
                <th className="status" onClick={() => sortData("status")}>
                  <span style={{ marginRight: 10 }}>Status</span>
                  {sortOrder.col === "status" ? renderArrow("status") : null}
                </th>
                <th
                  className="created-date"
                  onClick={() => sortData("create_date")}
                >
                  <span style={{ marginRight: 10 }}>Created Date</span>
                  {sortOrder.col === "create_date"
                    ? renderArrow("create_date")
                    : null}
                </th>
                <th
                  className="end-date"
                  onClick={() => sortData("complete_date")}
                >
                  <span style={{ marginRight: 5 }}>Completed Date</span>
                  {sortOrder.col === "complete_date"
                    ? renderArrow("complete_date")
                    : null}
                </th>
                <th className="approval">Approval Status</th>
              </tr>
            </thead>
            <tbody>{renderUsers()}</tbody>
          </table>
          <div className="refresh-button-div">
            <button onClick={handleRefresh} className="refresh-button">
              Refresh
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default AdminDashboard;
