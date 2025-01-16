import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import SignUp from './components/SignUp';
import AdminHome from './components/AdminHome';
import TeacherHome from './components/TeacherHome';
import StudentHome from './components/StudentHome';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Login and SignUp Pages */}
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />

        {/* Role-Based Home Pages */}
        <Route path="/admin" element={<AdminHome />} />
        <Route path="/teacher" element={<TeacherHome />} />
        <Route path="/student" element={<StudentHome />} />
      </Routes>
    </Router>
  );
};

export default App;
