import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './styles/AdminHome.css';

const AdminHome = () => {
  const [activeSection, setActiveSection] = useState<'create-class' | 'manage-users' | 'manage-classrooms'>('create-class');
  const [className, setClassName] = useState('');
  const [teacherEmail, setTeacherEmail] = useState('');
  const [users, setUsers] = useState<any[]>([]);
  const [classrooms, setClassrooms] = useState<any[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<any[]>([]);
  const navigate = useNavigate(); // Initialize useNavigate hook

  // Fetch users on component mount (for 'Manage Users' section)
  useEffect(() => {
    axios
      .get('http://127.0.0.1:8000/users', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      .then((response) => {
        const filtered = response.data.filter((user: any) => user.username !== 'admin');
        setUsers(filtered);
      })
      .catch((error) => console.error('Error fetching users:', error));
  }, []);

  // Fetch classrooms on component mount (for 'Manage Classrooms' section)
  useEffect(() => {
    axios
      .get('http://127.0.0.1:8000/classrooms', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      .then((response) => {
        setClassrooms(response.data.classrooms); // Update with classroom data
      })
      .catch((error) => console.error('Error fetching classrooms:', error));
  }, []);

  const handleTeacherEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const searchQuery = event.target.value;
    setTeacherEmail(searchQuery);

    if (searchQuery) {
      const filtered = users.filter((user: any) =>
        user.gmail.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredUsers(filtered);
    } else {
      setFilteredUsers([]);
    }
  };

  const handleDeleteUser = (userId: number) => {
    axios
      .delete(`http://127.0.0.1:8000/users/${userId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      .then((response) => {
        setUsers(users.filter((user) => user.id !== userId)); // Remove deleted user from the list
      })
      .catch((error) => console.error('Error deleting user:', error));
  };

  const handleCreateClass = () => {
    const teacherId = users.find((user) => user.gmail === teacherEmail)?.id;
    if (className && teacherId) {
      axios
        .post(
          'http://127.0.0.1:8000/classrooms/create',
          {
            id: 0,
            class_name: className,
            teacher_id: teacherId,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        )
        .then((response) => {
          console.log('Class created successfully:', response.data);
        })
        .catch((error) => console.error('Error creating class:', error));
    } else {
      console.log('Please fill in all the fields correctly.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove token from localStorage
    navigate('/'); // Redirect to home page (not /login)
  };

  // Handle delete classroom action
  const handleDeleteClass = (classroomId: number) => {
    axios
      .delete(`http://127.0.0.1:8000/classrooms/${classroomId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
      .then((response) => {
        // Remove the deleted classroom from the list
        setClassrooms(classrooms.filter((classroom) => classroom.id !== classroomId));
        console.log('Classroom deleted successfully:', response.data);
      })
      .catch((error) => console.error('Error deleting classroom:', error));
  };

  return (
    <div className="content">
      <div className="navbar">
        <button className="nav-button" onClick={() => setActiveSection('create-class')}>
          Create Class
        </button>
        <button className="nav-button" onClick={() => setActiveSection('manage-users')}>
          Manage Users
        </button>
        <button className="nav-button" onClick={() => setActiveSection('manage-classrooms')}>
          Manage Classrooms
        </button>
        <button className="nav-button" onClick={handleLogout}>
          Logout
        </button>
      </div>

      {activeSection === 'create-class' && (
        <div className="create-class-form">
          <h3>Create a New Class</h3>
          <div className="form-group">
            <label htmlFor="className">Class Name</label>
            <input
              type="text"
              id="className"
              className="form-control"
              value={className}
              onChange={(e) => setClassName(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="teacherEmail">Teacher Email</label>
            <input
              type="text"
              id="teacherEmail"
              className="teacher-search-input"
              value={teacherEmail}
              onChange={handleTeacherEmailChange}
              placeholder="Search for a teacher by email"
            />
            {filteredUsers.length > 0 && (
              <ul className="teacher-search-results">
                {filteredUsers.map((user) => (
                  <li
                    key={user.id}
                    className="search-result-item"
                    onClick={() => setTeacherEmail(user.gmail)}
                  >
                    {user.gmail}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <button className="btn btn-primary" onClick={handleCreateClass}>
            Create Class
          </button>
        </div>
      )}

      {activeSection === 'manage-users' && (
        <div className="manage-users">
          <h3>Manage Users</h3>
          <div className="user-list">
            {users.map((user) => (
              <div key={user.id} className="user-item">
                <p>{user.username} ({user.gmail})</p>
                <button className="btn btn-danger" onClick={() => handleDeleteUser(user.id)}>
                  Ban User
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeSection === 'manage-classrooms' && (
        <div className="manage-classrooms">
          <h3>Manage Classrooms</h3>
          <div className="classroom-list">
            {classrooms.length > 0 ? (
              classrooms.map((classroom: any) => {
                const teacher = users.find((user) => user.id === classroom.teacher_id);
                return (
                  <div key={classroom.id} className="classroom-item">
                    <p>Class Name: {classroom.class_name}</p>
                    {teacher ? (
                      <>
                        <p>Teacher: {teacher.username} ({teacher.gmail})</p>
                      </>
                    ) : (
                      <p>Teacher information not available</p>
                    )}
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDeleteClass(classroom.id)}
                    >
                      Delete Classroom
                    </button>
                  </div>
                );
              })
            ) : (
              <p>No classrooms found.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminHome;
