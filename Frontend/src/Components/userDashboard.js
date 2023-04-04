import { useEffect, useState } from "react";
import "../css/adminDashboard.css";
import NavBar from "../Pages/NavBar";
import data from "../Mock data/data";
import { FaArrowUp, FaArrowDown } from "react-icons/fa";

const UserDashboard = () => {
  const [users, setUsers] = useState(data);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [searchPhrase, setSearchPhrase] = useState("");
  const [sortOrder, setSortOrder] = useState({ col: "", order: "asc" });
  const [isPageLoading, setIsPageLoading] = useState(true);
  const taskMapToServiceRequest = {
    1: "IP Whitelist (Add)",
    2: "IP Whitelist (Remove)",
    3: "PSM Certificate Upload",
    4: "LDAP Certificate Upload",
  };
  // const formData = new FormData();
  // formData.set("support_id", 1);
  // useEffect(() => {
  //   async function fetchData() {
  //     await fetch("http://localhost:5000//getRequests", {
  //       mode: "cors",
  //       method: "POST",
  //       body: formData,
  //     }).then(async (response) => {
  //       const userList = await response.json();
  //       setUsers(userList);
  //       setFilteredUsers(userList);
  //     });
  //   }
  //   fetchData();
  // }, []);
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
  }, [searchPhrase]);

  const renderUsers = () => {
    return filteredUsers.map((user) => {
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
      return (
        <tr>
          <td className="cid">{user.customer_id}</td>
          {/* <td className="service-request">{user.task}</td> */}
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
          <td className="status">{user.status}</td>
          <td className="created-date">{created_date}</td>
          <td className="end-date">{completed_date}</td>
        </tr>
      );
    });
  };
  const sortData = (column) => {
    if (sortOrder.order === "asc") {
      if (column === "service_request") {
        const sortedData = [...data].sort((a, b) => {
          return taskMapToServiceRequest[a["task"]].toLowerCase() > taskMapToServiceRequest[b["task"]].toLowerCase() ? 1 : -1;
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
          return taskMapToServiceRequest[b["task"]].toLowerCase() > taskMapToServiceRequest[a["task"]].toLowerCase() ? 1 : -1;
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
        {/* <div className="container1">
          <div className="ring"></div>
          <div className="ring"></div>
          <div className="ring"></div>
          <p>Loading...</p>
        </div> */}
        <NavBar style={{ width: "100%" }} />
        <div className="table-container">
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
              </tr>
            </thead>
            <tbody>{renderUsers()}</tbody>
          </table>
        </div>
      </div>
    </>
  );
};

export default UserDashboard;
