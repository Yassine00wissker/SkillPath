import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { cn } from '../lib/utils';
import { Menu, X, User, LogOut, LayoutDashboard, Briefcase, GraduationCap, Map, BarChart } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
    const { user, logout } = useAuth();
    const location = useLocation();
    const [isOpen, setIsOpen] = useState(false);

    const navigation = [
        { name: 'Jobs', href: '/jobs', icon: Briefcase, current: location.pathname === '/jobs' },
        { name: 'Formations', href: '/formations', icon: GraduationCap, current: location.pathname === '/formations' },
    ];

    if (user) {
        if (user.role === 'admin') {
            navigation.unshift({ name: 'Dashboard', href: '/admin', icon: LayoutDashboard, current: location.pathname === '/admin' });
            navigation.push({ name: 'Parcours', href: '/admin/parcours', icon: Map, current: location.pathname === '/admin/parcours' });
            navigation.push({ name: 'Stats', href: '/admin/stats', icon: BarChart, current: location.pathname === '/admin/stats' });
        } else {
            navigation.unshift({ name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard, current: location.pathname === '/dashboard' });
            navigation.push({ name: 'My Path', href: '/path', icon: Map, current: location.pathname === '/path' });
            navigation.push({ name: 'Profile', href: '/profile', icon: User, current: location.pathname === '/profile' });
        }
    }

    return (
        <nav className="bg-surface border-b border-white/10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center">
                        <Link to="/" className="flex-shrink-0">
                            <span className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                                SkillPath
                            </span>
                        </Link>
                        <div className="hidden md:block">
                            <div className="ml-10 flex items-baseline space-x-4">
                                {navigation.map((item) => (
                                    <Link
                                        key={item.name}
                                        to={item.href}
                                        className={cn(
                                            item.current
                                                ? 'bg-primary/10 text-primary'
                                                : 'text-muted hover:bg-white/5 hover:text-white',
                                            'px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2 transition-colors'
                                        )}
                                    >
                                        <item.icon className="w-4 h-4" />
                                        {item.name}
                                    </Link>
                                ))}
                            </div>
                        </div>
                    </div>
                    <div className="hidden md:block">
                        <div className="ml-4 flex items-center md:ml-6">
                            {user ? (
                                <button
                                    onClick={logout}
                                    className="bg-white/5 p-2 rounded-full text-muted hover:text-white hover:bg-white/10 transition-colors"
                                >
                                    <LogOut className="w-5 h-5" />
                                </button>
                            ) : (
                                <div className="flex gap-4">
                                    <Link
                                        to="/login"
                                        className="text-muted hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                    >
                                        Login
                                    </Link>
                                    <Link
                                        to="/register"
                                        className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                                    >
                                        Register
                                    </Link>
                                </div>
                            )}
                        </div>
                    </div>
                    <div className="-mr-2 flex md:hidden">
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="bg-surface inline-flex items-center justify-center p-2 rounded-md text-muted hover:text-white hover:bg-white/5 focus:outline-none"
                        >
                            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                        </button>
                    </div>
                </div>
            </div>

            {isOpen && (
                <div className="md:hidden">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        {navigation.map((item) => (
                            <Link
                                key={item.name}
                                to={item.href}
                                className={cn(
                                    item.current ? 'bg-primary/10 text-primary' : 'text-muted hover:text-white hover:bg-white/5',
                                    'block px-3 py-2 rounded-md text-base font-medium flex items-center gap-2'
                                )}
                                onClick={() => setIsOpen(false)}
                            >
                                <item.icon className="w-4 h-4" />
                                {item.name}
                            </Link>
                        ))}
                        {!user && (
                            <>
                                <Link
                                    to="/login"
                                    className="text-muted hover:text-white block px-3 py-2 rounded-md text-base font-medium"
                                    onClick={() => setIsOpen(false)}
                                >
                                    Login
                                </Link>
                                <Link
                                    to="/register"
                                    className="text-muted hover:text-white block px-3 py-2 rounded-md text-base font-medium"
                                    onClick={() => setIsOpen(false)}
                                >
                                    Register
                                </Link>
                            </>
                        )}
                        {user && (
                            <button
                                onClick={() => { logout(); setIsOpen(false); }}
                                className="text-muted hover:text-white block w-full text-left px-3 py-2 rounded-md text-base font-medium flex items-center gap-2"
                            >
                                <LogOut className="w-4 h-4" />
                                Logout
                            </button>
                        )}
                    </div>
                </div>
            )}
        </nav>
    );
}
