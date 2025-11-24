import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  const user = localStorage.getItem('user');

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  // Optional: Verify token is still valid by checking expiry
  // For now, we'll just check if token exists
  // In production, you might want to decode the JWT and check expiry
  // or call an API endpoint to verify the token

  return children;
};

export default ProtectedRoute;

