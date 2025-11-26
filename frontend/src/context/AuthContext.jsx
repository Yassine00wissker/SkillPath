import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/client';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const response = await api.get('/users/me');
                    setUser(response.data);
                } catch (error) {
                    console.error("Auth check failed", error);
                    localStorage.removeItem('token');
                }
            }
            setLoading(false);
        };
        checkAuth();
    }, []);

    const login = async (email, password) => {
        const params = new URLSearchParams();
        params.append('username', email);
        params.append('password', password);
        const response = await api.post('/auth/login', params, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        const { access_token, user: userData } = response.data;
        localStorage.setItem('token', access_token);
        setUser(userData);
        return userData;
    };

    const register = async (data) => {
        // Transform full_name into separate first and last name fields expected by the backend
        const [nom, prenom = ''] = data.full_name ? data.full_name.split(' ', 2) : ['', ''];
        const payload = {
            nom,
            prenom,
            email: data.email,
            password: data.password,
            // competence and interests are optional; defaults will be applied by backend
        };
        const response = await api.post('/auth/register', payload);
        return response.data;
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
