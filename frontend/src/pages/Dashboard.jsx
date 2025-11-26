import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ArrowRight, Sparkles } from 'lucide-react';

export default function Dashboard() {
    const { user } = useAuth();

    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-white">
                    Welcome back, {user?.prenom || 'User'}!
                </h1>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="col-span-1 md:col-span-2 bg-gradient-to-br from-primary/20 to-secondary/20 border border-white/10 rounded-2xl p-8 relative overflow-hidden">
                    <div className="relative z-10">
                        <h2 className="text-2xl font-bold text-white mb-4">Discover Your Path</h2>
                        <p className="text-muted mb-6 max-w-lg">
                            Ready to take the next step in your career? Use our AI-powered path generator to create a personalized roadmap based on your goals.
                        </p>
                        <Link
                            to="/path"
                            className="inline-flex items-center gap-2 bg-white text-black px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-colors"
                        >
                            <Sparkles className="w-5 h-5" />
                            Generate Path
                        </Link>
                    </div>
                    <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-primary/30 to-secondary/30 blur-3xl rounded-full -translate-y-1/2 translate-x-1/2" />
                </div>

                <div className="bg-surface border border-white/10 rounded-2xl p-6">
                    <h3 className="text-lg font-semibold text-white mb-4">Quick Stats</h3>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center p-3 bg-background rounded-lg">
                            <span className="text-muted">Skills</span>
                            <span className="font-bold text-white">{user?.competence?.length || 0}</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-background rounded-lg">
                            <span className="text-muted">Interests</span>
                            <span className="font-bold text-white">{user?.interests?.length || 0}</span>
                        </div>
                    </div>
                    <Link
                        to="/profile"
                        className="block mt-6 text-center text-primary hover:text-primary-hover text-sm font-medium"
                    >
                        Update Profile →
                    </Link>
                </div>
            </div>
        </div>
    );
}
