import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, User, Loader2 } from 'lucide-react';

export default function Register() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const { register: registerUser } = useAuth();
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const onSubmit = async (data) => {
        setIsLoading(true);
        setError('');
        try {
            await registerUser(data);
            navigate('/login');
        } catch (err) {
            setError('Registration failed. Email might be taken.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-[80vh]">
            <div className="w-full max-w-md p-8 bg-surface rounded-2xl border border-white/10 shadow-xl">
                <h2 className="text-3xl font-bold text-center mb-8 text-white">Create Account</h2>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded-lg mb-6 text-sm text-center">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-muted mb-2">Full Name</label>
                        <div className="relative">
                            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
                            <input
                                {...register('full_name', { required: true })}
                                type="text"
                                className="w-full bg-background border border-white/10 rounded-lg py-2.5 pl-10 pr-4 text-white focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
                                placeholder="John Doe"
                            />
                        </div>
                        {errors.full_name && <span className="text-xs text-red-500 mt-1">Name is required</span>}
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-muted mb-2">Email Address</label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
                            <input
                                {...register('email', { required: true })}
                                type="email"
                                className="w-full bg-background border border-white/10 rounded-lg py-2.5 pl-10 pr-4 text-white focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
                                placeholder="you@example.com"
                            />
                        </div>
                        {errors.email && <span className="text-xs text-red-500 mt-1">Email is required</span>}
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-muted mb-2">Password</label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
                            <input
                                {...register('password', { required: true })}
                                type="password"
                                className="w-full bg-background border border-white/10 rounded-lg py-2.5 pl-10 pr-4 text-white focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
                                placeholder="••••••••"
                            />
                        </div>
                        {errors.password && <span className="text-xs text-red-500 mt-1">Password is required</span>}
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full bg-primary hover:bg-primary-hover text-white py-3 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2"
                    >
                        {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Create Account'}
                    </button>
                </form>

                <p className="mt-6 text-center text-muted text-sm">
                    Already have an account?{' '}
                    <Link to="/login" className="text-primary hover:text-primary-hover font-medium">
                        Sign in
                    </Link>
                </p>
            </div>
        </div>
    );
}
