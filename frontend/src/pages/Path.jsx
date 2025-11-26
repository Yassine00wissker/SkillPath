import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import TagInput from '../components/TagInput';
import { Sparkles, ArrowRight, BookOpen, Briefcase, CheckCircle, GraduationCap, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Path() {
    const { user } = useAuth();
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [goal, setGoal] = useState('');
    const [competences, setCompetences] = useState(user?.competence || []);
    const [interests, setInterests] = useState(user?.interests || []);
    const [pathData, setPathData] = useState(null);

    const generatePath = async () => {
        setLoading(true);
        try {
            const response = await api.post('/api/recommend/submit', {
                goal,
                competences,
                interests,
                mode: 'ai',
            });
            setPathData(response.data.skillpath);
            setStep(2);
        } catch (error) {
            console.error('Failed to generate path', error);
        } finally {
            setLoading(false);
        }
    };

    if (step === 1) {
        return (
            <div className="max-w-2xl mx-auto">
                <div className="text-center mb-10">
                    <h1 className="text-4xl font-bold text-white mb-4">Design Your Future</h1>
                    <p className="text-muted text-lg">
                        Let our AI analyze your profile and create a personalized roadmap to success.
                    </p>
                </div>

                <div className="bg-surface border border-white/10 rounded-2xl p-8 shadow-xl">
                    <div className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-muted mb-2">What is your main career goal?</label>
                            <textarea
                                value={goal}
                                onChange={(e) => setGoal(e.target.value)}
                                className="w-full bg-background border border-white/10 rounded-lg p-4 text-white focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors h-32 resize-none"
                                placeholder="e.g., Become a Senior Full Stack Developer specializing in React and Python..."
                            />
                        </div>

                        <TagInput
                            label="Your Current Skills"
                            tags={competences}
                            onChange={setCompetences}
                        />

                        <TagInput
                            label="Your Interests"
                            tags={interests}
                            onChange={setInterests}
                        />

                        <button
                            onClick={generatePath}
                            disabled={!goal || loading}
                            className="w-full bg-gradient-to-r from-primary to-secondary hover:opacity-90 text-white py-4 rounded-xl font-bold text-lg transition-all transform hover:scale-[1.02] flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-6 h-6 animate-spin" />
                                    Analyzing Career Paths...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-6 h-6" />
                                    Generate My Path
                                </>
                            )}
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto">
            <div className="flex items-center justify-between mb-8">
                <h1 className="text-3xl font-bold text-white">Your Personalized Path</h1>
                <button
                    onClick={() => setStep(1)}
                    className="text-muted hover:text-white transition-colors"
                >
                    Start Over
                </button>
            </div>

            <div className="space-y-8">
                {/* Recommended Jobs & Formations Summary */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-surface/50 border border-white/10 rounded-xl p-6">
                        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                            <Briefcase className="w-5 h-5 text-primary" />
                            Target Jobs
                        </h3>
                        <div className="space-y-3">
                            {pathData.recommended_jobs?.slice(0, 3).map((job, i) => (
                                <div key={i} className="bg-background p-3 rounded-lg border border-white/5">
                                    <div className="font-medium text-white">{job.titre}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="bg-surface/50 border border-white/10 rounded-xl p-6">
                        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                            <GraduationCap className="w-5 h-5 text-secondary" />
                            Recommended Courses
                        </h3>
                        <div className="space-y-3">
                            {pathData.recommended_formations?.slice(0, 3).map((formation, i) => (
                                <div key={i} className="bg-background p-3 rounded-lg border border-white/5">
                                    <div className="font-medium text-white">{formation.titre}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Timeline Steps */}
                <div className="relative border-l-2 border-white/10 ml-4 space-y-12 py-4">
                    {pathData.steps?.map((step, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="relative pl-8"
                        >
                            <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-primary border-4 border-background" />

                            <div className="bg-surface border border-white/10 rounded-xl p-6 hover:border-primary/30 transition-colors">
                                <div className="flex items-center justify-between mb-2">
                                    <h3 className="text-xl font-bold text-white">{step.title}</h3>
                                    <span className="text-xs font-medium px-2 py-1 rounded-full bg-white/5 text-muted">
                                        Step {index + 1}
                                    </span>
                                </div>
                                <p className="text-muted mb-4">{step.description}</p>

                                {step.resources && step.resources.length > 0 && (
                                    <div className="mt-4 pt-4 border-t border-white/5">
                                        <h4 className="text-sm font-medium text-white mb-2">Resources</h4>
                                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                            {step.resources.map((resource, rIndex) => (
                                                <div key={rIndex} className="flex items-center gap-2 text-sm text-muted bg-background/50 p-2 rounded-lg">
                                                    {resource.type === 'formation' ? <BookOpen className="w-4 h-4 text-secondary" /> : <Briefcase className="w-4 h-4 text-primary" />}
                                                    <span className="truncate">{resource.title}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </div>
    );
}
