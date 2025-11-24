import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import AdminRoute from './components/AdminRoute';
import ContentCreatorRoute from './components/ContentCreatorRoute';
import Header from './components/Header';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Jobs from './pages/Jobs';
import Formations from './pages/Formations';
import Profile from './pages/Profile';
import ManageFormations from './pages/ManageFormations';
import ManageJobs from './pages/ManageJobs';
import AdminDashboard from './pages/AdminDashboard';
import './styles/globals.css';

function App() {
  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gray-50">
                <Header />
                <Routes>
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/jobs" element={<Jobs />} />
                  <Route path="/formations" element={<Formations />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route
                    path="/manage-formations"
                    element={
                      <ContentCreatorRoute>
                        <ManageFormations />
                      </ContentCreatorRoute>
                    }
                  />
                  <Route
                    path="/manage-jobs"
                    element={
                      <ContentCreatorRoute>
                        <ManageJobs />
                      </ContentCreatorRoute>
                    }
                  />
                  <Route
                    path="/admin"
                    element={
                      <AdminRoute>
                        <AdminDashboard />
                      </AdminRoute>
                    }
                  />
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </div>
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
