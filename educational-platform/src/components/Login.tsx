import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/login',
        new URLSearchParams({
          grant_type: 'password',
          username: email,
          password: password,
          client_id: 'string', // Replace with actual client ID if needed
          client_secret: 'string', // Replace with actual client secret if needed
        }),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );

      const token = response.data.access_token;
      localStorage.setItem('token', token);
      localStorage.setItem('email', email);
      navigate('/home');
    } catch (error) {
      setErrorMessage('Invalid credentials');
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
        <button type="submit" className="btn btn-primary">
          Login
        </button>
      </form>
      <p>
        Don't have an account? <a href="/signup">Sign up</a>
      </p>
    </div>
  );
};

export default Login;
