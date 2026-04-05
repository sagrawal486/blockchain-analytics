import { useState, useEffect } from 'react';
import { RefreshCw, Plus, Wallet, AlertCircle, LogOut } from 'lucide-react';
import { walletAPI, transactionAPI, syncAPI, authAPI } from './api';
import SummaryCards from './components/SummaryCards';
import TransactionsTable from './components/TransactionsTable';
import AddWalletModal from './components/AddWalletModal';
import Login from './pages/Login';

export default function App() {
  const [user, setUser]                 = useState(null);
  const [wallets, setWallets]           = useState([]);
  const [activeWallet, setActiveWallet] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary]           = useState(null);
  const [loading, setLoading]           = useState(false);
  const [syncing, setSyncing]           = useState(false);
  const [showModal, setShowModal]       = useState(false);
  const [error, setError]               = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authAPI.me()
        .then(res => setUser(res.data))
        .catch(() => localStorage.removeItem('token'));
    }
  }, []);

  useEffect(() => {
    if (user) loadWallets();
  }, [user]);

  useEffect(() => {
    if (activeWallet) {
      loadTransactions(activeWallet);
      loadSummary(activeWallet);
    }
  }, [activeWallet]);

  const loadWallets = async () => {
    try {
      const res = await walletAPI.getAll();
      setWallets(res.data);
      if (res.data.length > 0 && !activeWallet) {
        setActiveWallet(res.data[0].address);
      }
    } catch (e) {
      setError('Failed to load wallets');
    }
  };

  const loadTransactions = async (address) => {
    setLoading(true);
    setError('');
    try {
      const res = await transactionAPI.getAll(address, 25);
      setTransactions(res.data);
    } catch (e) {
      if (e.response?.status === 404) setTransactions([]);
      else setError('Failed to load transactions');
    } finally {
      setLoading(false);
    }
  };

  const loadSummary = async (address) => {
    try {
      const res = await transactionAPI.getSummary(address);
      setSummary(res.data);
    } catch (e) {
      setSummary(null);
    }
  };

  const handleSync = async () => {
    if (!activeWallet) return;
    setSyncing(true);
    setError('');
    try {
      await syncAPI.trigger(activeWallet);
      await loadTransactions(activeWallet);
      await loadSummary(activeWallet);
    } catch (e) {
      setError('Sync failed. Check API connection.');
    } finally {
      setSyncing(false);
    }
  };

  const handleAddWallet = async (data) => {
    await walletAPI.add(data);
    await loadWallets();
    setActiveWallet(data.address.toLowerCase());
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setWallets([]);
    setTransactions([]);
    setSummary(null);
    setActiveWallet(null);
  };

  const shortAddr = (addr) => `${addr.slice(0, 8)}...${addr.slice(-6)}`;

  if (!user) return <Login onLogin={setUser} />;

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">

      <header className="border-b border-slate-800 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">

          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Wallet size={20} />
            </div>
            <div>
              <h1 className="font-bold text-lg">Blockchain Analytics</h1>
              <p className="text-slate-400 text-xs">Polygon Network</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-slate-400 text-sm">
              Hi, {user.username}
            </span>
            <button
              onClick={(() => setShowModal(true))}
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              <Plus size={16} />
              Add Wallet
            </button>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 bg-slate-700 hover:bg-slate-600 px-3 py-2 rounded-lg text-sm transition-colors"
            >
              <LogOut size={16} />
            </button>
          </div>

        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-6 space-y-6">

        {error && (
          <div className="flex items-center gap-2 bg-red-900 border border-red-800 rounded-lg px-4 py-3 text-red-400 text-sm">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        {wallets.length > 0 && (
          <div className="flex gap-2 flex-wrap">
            {wallets.map(w => (
              <button
                key={w.address}
                onClick={() => setActiveWallet(w.address)}
                className={activeWallet === w.address
                  ? "px-4 py-2 rounded-lg text-sm font-mono bg-blue-600 text-white"
                  : "px-4 py-2 rounded-lg text-sm font-mono bg-slate-800 text-slate-400 hover:bg-slate-700"
                }
              >
                {w.label || shortAddr(w.address)}
              </button>
            ))}
          </div>
        )}

        {wallets.length === 0 && (
          <div className="bg-slate-800 rounded-xl p-12 text-center border border-slate-600">
            <Wallet size={40} className="text-slate-600 mx-auto mb-3" />
            <p className="text-slate-400">No wallets added yet</p>
            <button
              onClick={() => setShowModal(true)}
              className="mt-4 bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg text-sm"
            >
              Add Your First Wallet
            </button>
          </div>
        )}

        {activeWallet && (
          <div className="space-y-6">

            <div className="flex justify-between items-center">
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider">Active Wallet</p>
                <p className="font-mono text-slate-300 text-sm mt-1">{activeWallet}</p>
              </div>
              <button
                onClick={handleSync}
                disabled={syncing}
                className="flex items-center gap-2 bg-slate-700 hover:bg-slate-600 disabled:opacity-50 px-4 py-2 rounded-lg text-sm transition-colors"
              >
                <RefreshCw size={14} className={syncing ? 'animate-spin' : ''} />
                {syncing ? 'Syncing...' : 'Sync Now'}
              </button>
            </div>

            <SummaryCards summary={summary} />

            <div>
              <div className="flex justify-between items-center mb-3">
                <h2 className="font-semibold text-slate-200">Recent Transactions</h2>
                <span className="text-xs text-slate-500">{transactions.length} shown</span>
              </div>
              {loading
                ? <div className="bg-slate-800 rounded-xl p-8 text-center text-slate-400">Loading transactions...</div>
                : <TransactionsTable transactions={transactions} />
              }
            </div>

          </div>
        )}

      </main>

      {showModal && (
        <AddWalletModal
          onAdd={handleAddWallet}
          onClose={() => setShowModal(false)}
        />
      )}

    </div>
  );
}
