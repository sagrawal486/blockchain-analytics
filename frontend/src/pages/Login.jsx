import { useState } from 'react';
import { authAPI } from '../api';
import { Wallet, Lock, User } from 'lucide-react';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');

  const handleLogin = async () => {
    if (!username || !password) {
      setError('Please enter username and password');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await authAPI.login(username, password);
      localStorage.setItem('token', res.data.access_token);
      onLogin(res.data);
    } catch (e) {
      setError('Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="bg-blue-600 w-14 h-14 rounded-xl flex items-center 
                          justify-center mx-auto mb-4">
            <Wallet size={28} />
          </div>
          <h1 className="text-2xl font-bold">Blockchain Analytics</h1>
          <p className="text-slate-400 text-sm mt-1">Sign in to your dashboard</p>
        </div>

        {/* Form */}
        <div className="bg-slate-800 rounded-xl p-8 border border-slate-700 space-y-5">
          
          <div>
            <label className="text-sm text-slate-400 block mb-2">Username</label>
            <div className="relative">
              <User size={16} className="absolute left-3 top-3 text-slate-400" />
              <input
                type        = "text"
                value       = {username}
                onChange    = {e => setUsername(e.target.value)}
                onKeyDown   = {e => e.key === 'Enter' && handleLogin()}
                placeholder = "admin"
                className   = "w-full bg-slate-700 border border-slate-600 rounded-lg pl-9 pr-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 transition-colors"
              />
            </div>
          </div>

          <div>
            <label className="text-sm text-slate-400 block mb-2">Password</label>
            <div className="relative">
              <Lock size={16} className="absolute left-3 top-3 text-slate-400" />
              <input
                type        = "password"
                value       = {password}
                onChange    = {e => setPassword(e.target.value)}
                onKeyDown   = {e => e.key === 'Enter' && handleLogin()}
                placeholder = "••••••••"
                className   = "w-full bg-slate-700 border border-slate-600 rounded-lg pl-9 pr-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 transition-colors"
              />
            </div>
          </div>

          {error && (
            <p className="text-red-400 text-sm bg-red-900/20 px-3 py-2 rounded-lg">
              {error}
            </p>
          )}

          <button
            onClick   = {handleLogin}
            disabled  = {loading}
            className = "w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-lg py-2.5 text-sm font-medium transition-colors"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <p className="text-center text-slate-500 text-xs">
            Default: admin / admin123
          </p>
        </div>
      </div>
    </div>
  );
}
