import { Navigate } from 'react-router-dom';

const AdminRoute = ({ children }) => {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const admin = JSON.parse(localStorage.getItem('admin') || 'null');
  const token = localStorage.getItem('token');

  // Check if user is admin or if admin token exists
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (user && user.role === 'admin') {
    return children;
  }

  if (admin) {
    return children;
  }

  // Not an admin, redirect to dashboard
  return <Navigate to="/dashboard" replace />;
};

export default AdminRoute;

