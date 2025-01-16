import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import AdminHome from './AdminHome';
import TeacherHome from './TeacherHome';
import StudentHome from './StudentHome';

const Home: React.FC = () => {
  const [role, setRole] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');
    
    if (token && email) {
      // Fetch user details from the backend using the token
      axios
        .get('http://127.0.0.1:8000/users', {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          // Find the user by email
          const user = response.data.find((u: any) => u.gmail === email);
          if (user) {
            // Set the user's role based on the backend data
            if (user.global_admin) {
              setRole('admin');
            } else if (user.teacher) {
              setRole('teacher');
            } else {
              setRole('student');
            }
          }
        })
        .catch((error) => {
          console.error('Error fetching user data:', error);
        });
    } else {
      navigate('/'); // Redirect to login if no token or email is found
    }
  }, [navigate]);

  // Render different home components based on the role
  if (role === 'admin') {
    return <AdminHome />;
  } else if (role === 'teacher') {
    return <TeacherHome />;
  } else if (role === 'student') {
    return <StudentHome />;
  }

  // Show a loading state until the role is determined
  return <div>Loading...</div>;
};

export default Home;
