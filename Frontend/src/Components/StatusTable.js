import { useEffect, useState } from "react";
import { data } from "../Components/Reports";
import "../css/StatusTable.css";
import NavBar from "../Pages/NavBar";

const StatusTable = () => {
  const [users, setUsers] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [searchPhrase, setSearchPhrase] = useState("");
  const [sortOrder, setSortOrder] = useState({ col: "", order: "asc" });
  const [isPageLoading,setIsPageLoading]=useState(true);
  const taskMapToServiceRequest = {
    1: "IP Whitelist (Add)",
    2: "IP Whitelist (Remove)",
    3: "LDAP Certificate Upload",
    4: "PSM Certificate",
  };
  const formData = new FormData();
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
  useEffect(()=>{
    if(users.length > 0){
      document.body.style.filter = "blur(0px)";
    }
  },[users])
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
          {/* {(user.status === "SUCCESS" && (
            <td className="status" style={{ color: "green" }}>
              {user.Status}
            </td>
          )) ||
            (user.Status === "FAILED" && (
              <td className="status" style={{ color: "red" }}>
                {user.Status}
              </td>
            )) ||
            (user.Status === "IN_PROGRESS" && (
              <td className="status" style={{ color: "#e66b19" }}>
                {user.Status}
              </td>
            )) ||
            (user.Status === "WAITING_FOR_APPROVAL" && (
              <td className="status" style={{ color: "#f5b800" }}>
                {user.Status}
              </td>
            )) ||
            (user.Status === "DENIED" && (
              <td className="status" style={{ color: "grey" }}>
                {user.Status}
              </td>
            ))} */}

          <td className="created-date">{created_date}</td>
          <td className="end-date">{completed_date}</td>
        </tr>
      );
    });
  };
  const search = () => {
    const matchedUsers = users.filter((user) => {
      return (
        taskMapToServiceRequest[user.task]
          .toLowerCase()
          .includes(searchPhrase.toLowerCase()) ||
        user.status.toLowerCase().includes(searchPhrase.toLowerCase()) ||
        user.customer_id.toLowerCase().includes(searchPhrase.toLowerCase())
      );
    });
    setUsers(matchedUsers);
  };
  const sortData = (column) => {
    if (sortOrder.order === "asc") {
      const sortedData = [...data].sort((a, b) =>
        a[column].toLowerCase() > b[column].toLowerCase() ? 1 : -1
      );
      setUsers(sortedData);
      setSortOrder({ col: column, order: "desc" });
    }
    if (sortOrder.order === "desc") {
      const sortedData = [...data].sort((a, b) =>
        a[column].toLowerCase() < b[column].toLowerCase() ? 1 : -1
      );
      setUsers(sortedData);
      setSortOrder({ col: column, order: "asc" });
    }
  };
  // const renderArrow = (column) => {
  //   if (sortOrder.order === "asc" && sortOrder.col === column) {
  //     return <FaArrowUp />;
  //   } else if (sortOrder.order === "desc" && sortOrder.col === column) {
  //     return <FaArrowDown />;
  //   } else {
  //     return null;
  //   }
  // };
  return (
    <>
      <div className="container">
        <div className="container1">
          <div className="ring"></div>
          <div className="ring"></div>
          <div className="ring"></div>
          <p>Loading...</p>
        </div>
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
                  onClick={() => sortData("Service_Request")}
                >
                  <span style={{ marginRight: 10 }}>Service Request</span>
                  {/* {sortOrder.col === "Service_Request"
                    ? renderArrow("Service_Request")
                    : null} */}
                </th>
                <th className="status" onClick={() => sortData("Status")}>
                  <span style={{ marginRight: 10 }}>Status</span>
                  {/* {sortOrder.col === "Status" ? renderArrow("Status") : null} */}
                </th>
                <th className="created-date">Created Date</th>
                <th className="end-date">Completed Date</th>
              </tr>
            </thead>
            <tbody>{renderUsers()}</tbody>
          </table>
        </div>
      </div>
    </>
  );
};

export default StatusTable;
