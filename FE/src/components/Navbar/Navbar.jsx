import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { MessageCircle, BarChart3, Cake } from 'lucide-react';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <Cake className="brand-icon" />
          <span className="brand-text">Bakery Bot</span>
        </div>
        
        <div className="navbar-menu">
          <Link 
            to="/chat" 
            className={`navbar-item ${location.pathname === '/chat' ? 'active' : ''}`}
          >
            <MessageCircle size={20} />
            <span>Chat Bot</span>
          </Link>
          
          <Link 
            to="/admin" 
            className={`navbar-item ${location.pathname === '/admin' ? 'active' : ''}`}
          >
            <BarChart3 size={20} />
            <span>Thống Kê</span>
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 