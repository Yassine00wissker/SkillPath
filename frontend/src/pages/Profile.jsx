import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import TagInput from '../components/TagInput';
import { User, Mail, Save, Loader2 } from 'lucide-react';

export default function Profile() {
    const { user } = useAuth();
    const { register, handleSubmit, setValue } = useForm();
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState('');
    const [competences, setCompetences] = useState([]);
    const [interests, setInterests] = useState([]);

    useEffect(() => {
        if (user) {
            setValue('nom', user.nom);
            setValue('prenom', user.prenom);
            setValue('email', user.email);
            setCompetences(user.competence || []);
            setInterests(user.interests || []);
        }
    }, [user, setValue]);

    const onSubmit = async (data) => {
        setLoading(true);
        setSuccess('');
        try {
            await api.put('/users/me', {
                ...data,
                competence: competences,
                interests: interests,
            });
            setSuccess('Profile updated successfully!');
        } catch (error) {
            console.error('Failed to update profile', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto">
            <h1 className="text-3xl font-bold text-white mb-8">My Profile</h1>

            <div className="bg-surface border border-white/10 rounded-2xl p-8">
                {success && (
                    <div className="bg-green-500/10 border border-green-500/50 text-green-500 p-3 rounded-lg mb-6 text-sm">
                        {success}
                    </div>
                )}

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-muted mb-2">First Name</label>
                            <div className="relative">
                                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
                                <input
                                    {...register('prenom')}
                                    type="text"
                                    className="w-full bg-background border border-white/10 rounded-lg py-2.5 pl-10 pr-4 text-white focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
                                />
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-muted mb-2">Last Name</label>
                            <div className="relative">
                                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
                                <input
                                    {...register('nom')}
                                    type="text"
                                    className="w-full bg-background border border-white/10 rounded-lg py-2.5 pl-10 pr-4 text-white focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
                                />
                            </div>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-muted mb-2">Email Address</label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
                            <input
                                {...register('email')}
                                type="email"
                                disabled
                                className="w-full bg-background/50 border border-white/10 rounded-lg py-2.5 pl-10 pr-4 text-muted cursor-not-allowed"
                            />
                        </div>
                    </div>

                    <div className="border-t border-white/10 pt-6">
                        <h3 className="text-lg font-semibold text-white mb-4">Skills & Interests</h3>
                        <div className="space-y-6">
                            <TagInput
                                label="Competences"
                                tags={competences}
                                onChange={setCompetences}
                            />
                            <TagInput
                                label="Interests"
                                tags={interests}
                                onChange={setInterests}
                            />
                        </div>
                    </div>

                    <div className="pt-4">
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-primary hover:bg-primary-hover text-white py-3 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2"
                        >
                            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
                                <>
                                    <Save className="w-5 h-5" />
                                    Save Changes
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
