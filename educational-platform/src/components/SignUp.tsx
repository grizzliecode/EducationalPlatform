import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const SignUp: React.FC = () => {
  const [username, setUsername] = useState('');
  const [gmail, setGmail] = useState('');
  const [password, setPassword] = useState('');
  const [isTeacher, setIsTeacher] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();

    const user = {
      user_id: 0,
      username: username,
      password: password,
      gmail: gmail,
      global_admin: false, // Default global_admin to false
      teacher: isTeacher,
    };

    try {
      await axios.post('http://127.0.0.1:8000/users/create', user, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      navigate('/'); // Redirect to login after successful sign-up
    } catch (error) {
      setErrorMessage('Error creating account');
    }
  };

  return (
    <div className="signup-container">
      <h2>Sign Up</h2>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <form onSubmit={handleSignUp}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="gmail">Gmail</label>
          <input
            type="email"
            id="gmail"
            className="form-control"
            value={gmail}
            onChange={(e) => setGmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="form-check">
          <input
            type="checkbox"
            id="isTeacher"
            className="form-check-input"
            checked={isTeacher}
            onChange={() => setIsTeacher(!isTeacher)}
          />
          <label className="form-check-label" htmlFor="isTeacher">
            Are you a Teacher?
          </label>
        </div>
        <button type="submit" className="btn btn-primary">
          Sign Up
        </button>
      </form>
      <p>
        Already have an account? <button className="btn btn-link" onClick={() => navigate('/')}>Back to Login</button>
      </p>
    </div>
  );
};

export default SignUp;
