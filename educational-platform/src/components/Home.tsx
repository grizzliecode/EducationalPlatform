import React from 'react';

const Home: React.FC = () => {
  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container">
          <a className="navbar-brand" href="/">Educational Platform</a>
        </div>
      </nav>
      <div className="container mt-5">
        <h1>Welcome to the Home Page!</h1>
      </div>
    </div>
  );
};

export default Home;
