import { useState, useEffect } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import api from '../api/client';
import DataTable from '../components/DataTable';
import { LayoutDashboard, Briefcase, GraduationCap, Download, Plus, Users, Layers } from 'lucide-react';

function AdminStats() {
    const [stats, setStats] = useState(null);

    useEffect(() => {
        api.get('/api/admin/statistics').then(res => setStats(res.data));
    }, []);

    if (!stats) return <div>Loading stats...</div>;

    const cards = [
        { label: 'Total Users', value: stats.total_users, icon: Users, color: 'text-blue-500', bg: 'bg-blue-500/10' },
        { label: 'Formations', value: stats.total_formations, icon: GraduationCap, color: 'text-green-500', bg: 'bg-green-500/10' },
        { label: 'Jobs', value: 12, icon: Briefcase, color: 'text-purple-500', bg: 'bg-purple-500/10' }, // Mocked as endpoint might not return it yet
        { label: 'Categories', value: stats.total_categories, icon: Layers, color: 'text-orange-500', bg: 'bg-orange-500/10' },
    ];

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {cards.map((card) => (
                    <div key={card.label} className="bg-surface border border-white/10 rounded-xl p-6">
                        <div className="flex items-center justify-between mb-4">
                            <div className={`p-3 rounded-lg ${card.bg} ${card.color}`}>
                                <card.icon className="w-6 h-6" />
                            </div>
                        </div>
                        <div className="text-3xl font-bold text-white mb-1">{card.value}</div>
                        <div className="text-sm text-muted">{card.label}</div>
                    </div>
                ))}
            </div>

            <div className="bg-surface border border-white/10 rounded-xl p-6">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold text-white">Database Management</h3>
                    <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-colors">
                        <Download className="w-4 h-4" />
                        Export Database
                    </button>
                </div>
                <p className="text-muted">
                    Export the entire database as a JSON file for backup or analysis purposes.
                </p>
            </div>
        </div>
    );
}

function AdminJobs() {
    const [jobs, setJobs] = useState([]);

    useEffect(() => {
        api.get('/jobs').then(res => setJobs(res.data));
    }, []);

    const columns = [
        { key: 'title', label: 'Title' },
        { key: 'company', label: 'Company' },
        { key: 'location', label: 'Location' },
        { key: 'salary_range', label: 'Salary' },
    ];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-white">Manage Jobs</h2>
                <button className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary-hover text-white rounded-lg transition-colors">
                    <Plus className="w-4 h-4" />
                    Add Job
                </button>
            </div>
            <DataTable
                columns={columns}
                data={jobs}
                onEdit={(row) => console.log('Edit', row)}
                onDelete={(row) => console.log('Delete', row)}
            />
        </div>
    );
}

function AdminFormations() {
    const [formations, setFormations] = useState([]);

    useEffect(() => {
        api.get('/formations').then(res => setFormations(res.data));
    }, []);

    const columns = [
        { key: 'titre', label: 'Title' },
        { key: 'duration', label: 'Duration' },
        { key: 'price', label: 'Price' },
    ];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-white">Manage Formations</h2>
                <button className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary-hover text-white rounded-lg transition-colors">
                    <Plus className="w-4 h-4" />
                    Add Formation
                </button>
            </div>
            <DataTable
                columns={columns}
                data={formations}
                onEdit={(row) => console.log('Edit', row)}
                onDelete={(row) => console.log('Delete', row)}
            />
        </div>
    );
}

export default function AdminDashboard() {
    const location = useLocation();

    const tabs = [
        { name: 'Overview', path: '/admin', icon: LayoutDashboard },
        { name: 'Jobs', path: '/admin/jobs', icon: Briefcase },
        { name: 'Formations', path: '/admin/formations', icon: GraduationCap },
    ];

    return (
        <div className="space-y-8">
            <h1 className="text-3xl font-bold text-white">Admin Dashboard</h1>

            <div className="flex space-x-1 bg-surface p-1 rounded-xl border border-white/10 w-fit">
                {tabs.map((tab) => (
                    <Link
                        key={tab.name}
                        to={tab.path}
                        className={`
              flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all
              ${location.pathname === tab.path
                                ? 'bg-primary text-white shadow-lg'
                                : 'text-muted hover:text-white hover:bg-white/5'}
            `}
                    >
                        <tab.icon className="w-4 h-4" />
                        {tab.name}
                    </Link>
                ))}
            </div>

            <Routes>
                <Route path="/" element={<AdminStats />} />
                <Route path="/jobs" element={<AdminJobs />} />
                <Route path="/formations" element={<AdminFormations />} />
            </Routes>
        </div>
    );
}
