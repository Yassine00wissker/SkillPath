import { useState, useEffect } from 'react';
import api from '../api/client';
import { GraduationCap, Clock, BookOpen, Star } from 'lucide-react';

export default function Formations() {
    const [formations, setFormations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchFormations = async () => {
            try {
                const response = await api.get('/formations');
                setFormations(response.data);
            } catch (error) {
                console.error('Failed to fetch formations', error);
            } finally {
                setLoading(false);
            }
        };
        fetchFormations();
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
                <h1 className="text-3xl font-bold text-white">Available Formations</h1>
                <div className="text-muted">{formations.length} courses</div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {formations.map((formation) => (
                    <div key={formation.id} className="bg-surface border border-white/5 rounded-xl overflow-hidden hover:border-secondary/50 transition-all group">
                        <div className="h-48 bg-gradient-to-br from-surface to-background relative">
                            {/* Placeholder for course image */}
                            <div className="absolute inset-0 flex items-center justify-center text-secondary/20">
                                <GraduationCap className="w-16 h-16" />
                            </div>
                            <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-md px-2 py-1 rounded-md text-xs font-medium text-white flex items-center">
                                <Star className="w-3 h-3 text-yellow-500 mr-1" />
                                4.8
                            </div>
                        </div>

                        <div className="p-6">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-xs font-medium text-secondary uppercase tracking-wider">
                                    {formation.category?.name || 'Development'}
                                </span>
                                <span className="text-xs text-muted flex items-center">
                                    <Clock className="w-3 h-3 mr-1" />
                                    {formation.duration || '4 weeks'}
                                </span>
                            </div>

                            <h3 className="text-xl font-bold text-white mb-2">{formation.title}</h3>
                            <p className="text-muted text-sm mb-4 line-clamp-2">{formation.description}</p>

                            <div className="flex items-center justify-between mt-4 pt-4 border-t border-white/5">
                                <div className="flex items-center text-sm text-white font-medium">
                                    <BookOpen className="w-4 h-4 mr-2 text-muted" />
                                    {formation.lessons_count || 12} Lessons
                                </div>
                                <button className="text-sm font-medium text-secondary hover:text-secondary-hover transition-colors">
                                    Enroll Now →
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
