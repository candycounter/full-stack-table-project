import React, { useState } from 'react';
import Popup from 'reactjs-popup';
import NumberFormat from 'react-number-format';
import './App.css';

function App() {
  const [info, setInfo] = useState([])
  const [addedInfo, setAddedInfo] = useState({})
  const [removeInfo, setRemoveInfo] = useState({})
  const [updateInfo, setUpdateInfo] = useState({})
  const [show, setShow] = useState(false)
  const [buttonName, setButtonName] = useState("View Employee List")
  const viewEmployeeList = (event) => {

       fetch('http://localhost:5000/getemployees', {
            'method':'GET',
            headers : {
                'Content-Type': 'application/json'
          },
        })
        .then(response => response.json())
        .then(data => {
            setInfo(data)
            setShow(!show)
            showBoolean()
        })
   }

  const handleAddConfirm = (event) => {
        event.preventDefault();
        console.log(addedInfo);
        fetch('http://localhost:5000/addemployee', {
            'method':'POST',
            headers : {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(addedInfo)
        }).then(response => response.json())
        .then(data => {
            setInfo(data)
        })
  }

    const handleRemoveConfirm = (event) => {
        event.preventDefault();
        console.log(removeInfo);
        fetch('http://localhost:5000/removeemployee', {
            'method':'POST',
            headers : {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(removeInfo)
        }).then(response => response.json())
        .then(data => {
            setInfo(data)
        })
  }

  const handleUpdateConfirm = (event) => {
       event.preventDefault()
       console.log(updateInfo)
       fetch('http://localhost:5000/updateemployee', {
           'method': 'POST',
           headers: {
                'Content-Type': 'application/json'
           },
           body: JSON.stringify(updateInfo)
       }).then(response => response.json())
       .then(data => {
            setInfo(data)
       })
  }

  const showBoolean = (event) => {
      if(!show){
        setButtonName("Hide Employee List")
    } else {
        setButtonName("View Employee List")
    }
  }

  const handleAdd = (event) => {
        const name = event.target.name;
        const value = event.target.value;


        setAddedInfo(inputs => (
            {
                ...inputs,
                [name]: value
            }
        ))
  }

  const handleRemove = (event) => {
        const name = event.target.name
        const value = event.target.value
        setRemoveInfo(inputs => (
            {
                ...inputs,
                [name]: value
            }
        ))
  }

  const handleUpdate = (event) => {
        const name = event.target.name
        const value = event.target.value

        setUpdateInfo(inputs => (
        {
            ...inputs,
            [name]: value
        }
        ))
  }
  function ShowTable(){
    return (
        <table>
        <tr>
          <th>Name</th>
          <th>Role</th>
          <th>Employee ID</th>
          <th>Education</th>
          <th>Year Hired</th>
        </tr>
        {info.map((val, key) => {
          return (
            <tr key={key}>
              <td>{val["name"]}</td>
              <td>{val["role"]}</td>
              <td>{val["id"]}</td>
              <td>{val["education"]}</td>
              <td>{val["year_hired"]}</td>
            </tr>
          )
        })}
      </table>
     )
  }
  return (
    <div className="App">
       <Popup trigger={<button> Add Employee </button>}
        position="bottom center">
        <form onSubmit = {handleAddConfirm}>
        <p>
            First Name:
            <input
            type = "text"
            name = "first"
            onChange = {handleAdd}
            required/>
        </p>
        <p>
            Last Name:
            <input
            type = "text"
            name = "last"
            onChange = {handleAdd}
            required/>
        </p>
        <p>
            Role:
            <input
            type = "text"
            name = "role"
            onChange = {handleAdd}
            required/>
        </p>
        <p>
            ID:
            <NumberFormat
            format="#########"
            mask="_"
            name="employee_id"
            onChange = {handleAdd}
            required />
        </p>
        <p>
            Education:
            <input
            type = "text"
            name = "education"
            onChange = {handleAdd}
            required/>
        </p>
        <p>
            Year Hired:
            <NumberFormat
            format="####"
            mask="_"
            name = "year_hired"
            onChange = {handleAdd}
            required />
        </p>
        <button>Confirm</button>
    </form>
    </Popup>
   <Popup trigger={<button> Remove Employee </button>}
        position="bottom center">
        <form onSubmit = {handleRemoveConfirm}>
                <p>
                    First Name:
                    <input
                    type = "text"
                    name = "first"
                    onChange = {handleRemove}
                    required/>
                </p>
                <p>
                    Last Name:
                    <input
                    type = "text"
                    name = "last"
                    onChange = {handleRemove}
                    required/>
                </p>
                <p>
                    ID:
                    <NumberFormat
                    format="#########"
                    mask="_"
                    name="employee_id"
                    onChange = {handleRemove}
                    required />
                </p>
                <button>Confirm</button>
            </form>
        </Popup>
        <button onClick = {viewEmployeeList}>{buttonName}</button>
        <Popup trigger={<button> Update Employee Role </button>} position="bottom center">
            <form onSubmit = {handleUpdateConfirm}>
                <p>
                    ID:
                    <NumberFormat
                    format="#########"
                    mask="_"
                    name="employee_id"
                    onChange = {handleUpdate}
                    required />
                </p>
                <p>
                    New Role:
                    <input
                    type = "text"
                    name="role"
                    onChange = {handleUpdate}
                    required />
                </p>
                <button>Confirm</button>
            </form>
        </Popup>
      {show ? <ShowTable /> : null}
    </div>
  );
}

export default App;
