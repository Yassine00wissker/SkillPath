import { Link, useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || 'null');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <header className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <Link to="/dashboard" className="text-2xl font-bold text-indigo-600">
            SkillPath
          </Link>
          <nav className="flex items-center gap-6">
            <Link
              to="/dashboard"
              className="text-gray-700 hover:text-indigo-600 transition-colors"
            >
              Dashboard
            </Link>
            <Link
              to="/jobs"
              className="text-gray-700 hover:text-indigo-600 transition-colors"
            >
              Jobs
            </Link>
            <Link
              to="/formations"
              className="text-gray-700 hover:text-indigo-600 transition-colors"
            >
              Formations
            </Link>
            {user && (user.role === 'content_creator' || user.role === 'admin') && (
              <>
                <Link
                  to="/manage-formations"
                  className="text-gray-700 hover:text-indigo-600 transition-colors"
                >
                  Manage Formations
                </Link>
                <Link
                  to="/manage-jobs"
                  className="text-gray-700 hover:text-indigo-600 transition-colors"
                >
                  Manage Jobs
                </Link>
              </>
            )}
            {user && user.role === 'admin' && (
              <Link
                to="/admin"
                className="text-gray-700 hover:text-indigo-600 transition-colors font-semibold"
              >
                Admin Panel
              </Link>
            )}
            {user && (
              <span className="text-gray-600 text-sm">
                {user.prenom} {user.nom}
              </span>
            )}
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition-colors"
            >
              Logout
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;

