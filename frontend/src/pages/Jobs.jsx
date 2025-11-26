import { useState, useEffect } from 'react';
import api from '../api/client';
import { Briefcase, MapPin, DollarSign, Clock } from 'lucide-react';

export default function Jobs() {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const response = await api.get('/jobs');
                setJobs(response.data);
            } catch (error) {
                console.error('Failed to fetch jobs', error);
            } finally {
                setLoading(false);
            }
        };
        fetchJobs();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[50vh]">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
        );
    }

    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-white">Explore Jobs</h1>
                <div className="text-muted">{jobs.length} open positions</div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {jobs.map((job) => (
                    <div key={job.id} className="bg-surface border border-white/5 rounded-xl p-6 hover:border-primary/50 transition-all group">
                        <div className="flex items-start justify-between mb-4">
                            <div className="p-3 bg-primary/10 rounded-lg text-primary group-hover:bg-primary group-hover:text-white transition-colors">
                                <Briefcase className="w-6 h-6" />
                            </div>
                            <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-white/5 text-muted">
                                Full Time
                            </span>
                        </div>

                        <h3 className="text-xl font-bold text-white mb-2">{job.title}</h3>
                        <p className="text-muted text-sm mb-4 line-clamp-2">{job.description}</p>

                        <div className="space-y-2 mb-6">
                            <div className="flex items-center text-sm text-muted">
                                <MapPin className="w-4 h-4 mr-2" />
                                {job.location || 'Remote'}
                            </div>
                            <div className="flex items-center text-sm text-muted">
                                <DollarSign className="w-4 h-4 mr-2" />
                                {job.salary_range || 'Competitive'}
                            </div>
                        </div>

                        <button className="w-full py-2 rounded-lg bg-white/5 text-white font-medium hover:bg-white/10 transition-colors">
                            View Details
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
