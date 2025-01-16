import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = localStorage.getItem('token');
  
  if (!token) {
    // Redirect to login if the user is not authenticated
    return <Navigate to="/" />;
  }

  return <>{children}</>;
};

export default PrivateRoute;
