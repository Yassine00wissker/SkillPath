import { Navigate } from 'react-router-dom';

const ContentCreatorRoute = ({ children }) => {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const admin = JSON.parse(localStorage.getItem('admin') || 'null');
  const token = localStorage.getItem('token');

  // Check if user has content creator or admin role
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (user && (user.role === 'content_creator' || user.role === 'admin')) {
    return children;
  }

  if (admin) {
    return children;
  }

  // Not authorized, redirect to dashboard
  return <Navigate to="/dashboard" replace />;
};

export default ContentCreatorRoute;

