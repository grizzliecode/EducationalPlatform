import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      // Format the request body
      const data = new URLSearchParams();
      data.append('grant_type', 'password');
      data.append('username', email); // Username from the form
      data.append('password', password); // Password from the form
      data.append('scope', '');
      data.append('client_id', 'string'); // Fixed value based on the API
      data.append('client_secret', 'string'); // Fixed value based on the API

      // Make the POST request
      const response = await axios.post('http://127.0.0.1:8000/login', data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          Accept: 'application/json',
        },
      });

      const token = response.data.access_token; // Assuming the token is in `access_token`
      localStorage.setItem('token', token); // Store the JWT token
      navigate('/home'); // Redirect to home page
    } catch (err: any) {
      console.error(err);
      setError('Login failed. Please check your credentials and try again.');
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-4">
          <h2 className="text-center">Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                className="form-control"
                placeholder="Enter email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                className="form-control"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {error && <div className="alert alert-danger">{error}</div>}
            <button type="submit" className="btn btn-primary w-100">Login</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
