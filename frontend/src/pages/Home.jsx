import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle, Zap, Shield } from 'lucide-react';

export default function Home() {
    return (
        <div className="space-y-20">
            {/* Hero Section */}
            <section className="relative overflow-hidden pt-16 pb-20 lg:pt-24 lg:pb-28">
                <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="text-center">
                        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl mb-6">
                            Master Your Future with{' '}
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                                SkillPath
                            </span>
                        </h1>
                        <p className="mx-auto mt-4 max-w-2xl text-lg text-muted mb-10">
                            AI-powered career guidance tailored to your unique skills and goals.
                            Discover your perfect path, find the right training, and land your dream job.
                        </p>
                        <div className="flex justify-center gap-4">
                            <Link
                                to="/register"
                                className="bg-primary hover:bg-primary-hover text-white px-8 py-3 rounded-lg font-semibold text-lg transition-all transform hover:scale-105 flex items-center gap-2"
                            >
                                Get Started <ArrowRight className="w-5 h-5" />
                            </Link>
                            <Link
                                to="/jobs"
                                className="bg-surface hover:bg-white/5 text-white px-8 py-3 rounded-lg font-semibold text-lg border border-white/10 transition-all"
                            >
                                Explore Jobs
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-16 bg-surface/30 rounded-3xl border border-white/5">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                        <div className="text-center p-6 rounded-xl bg-surface border border-white/5 hover:border-primary/50 transition-colors">
                            <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mx-auto mb-4 text-primary">
                                <Zap className="w-6 h-6" />
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">AI Recommendations</h3>
                            <p className="text-muted">
                                Get personalized career paths and training suggestions based on your profile and goals.
                            </p>
                        </div>
                        <div className="text-center p-6 rounded-xl bg-surface border border-white/5 hover:border-secondary/50 transition-colors">
                            <div className="w-12 h-12 bg-secondary/20 rounded-lg flex items-center justify-center mx-auto mb-4 text-secondary">
                                <CheckCircle className="w-6 h-6" />
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">Curated Content</h3>
                            <p className="text-muted">
                                Access a vast library of verified jobs and formations from top providers.
                            </p>
                        </div>
                        <div className="text-center p-6 rounded-xl bg-surface border border-white/5 hover:border-primary/50 transition-colors">
                            <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mx-auto mb-4 text-primary">
                                <Shield className="w-6 h-6" />
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">Verified Paths</h3>
                            <p className="text-muted">
                                Follow structured learning paths designed by industry experts and AI analysis.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
