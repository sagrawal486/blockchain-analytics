import { useState } from 'react';
import { X } from 'lucide-react';

export default function AddWalletModal({ onAdd, onClose }) {
  const [address, setAddress] = useState('');
  const [label,   setLabel]   = useState('');
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState('');

  const handleSubmit = async () => {
    if (!address.startsWith('0x') || address.length !== 42) {
      setError('Please enter a valid Ethereum/Polygon wallet address');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await onAdd({ address, label, chain: 'matic-mainnet' });
      onClose();
    } catch (e) {
      setError(e.response?.data?.detail || 'Failed to add wallet');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-slate-800 rounded-xl p-6 w-full max-w-md border border-slate-700">

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-lg font-semibold">Add Wallet to Monitor</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X size={20} />
          </button>
        </div>

        <div className="space-y-4">

          <div>
            <label className="text-sm text-slate-400 block mb-1">
              Wallet Address *
            </label>
            <input
              type="text"
              value={address}
              onChange={e => setAddress(e.target.value)}
              placeholder="0x..."
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="text-sm text-slate-400 block mb-1">
              Label (optional)
            </label>
            <input
              type="text"
              value={label}
              onChange={e => setLabel(e.target.value)}
              placeholder="e.g. Company Treasury"
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
            />
          </div>

          {error && (
            <p className="text-red-400 text-sm">{error}</p>
          )}

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-lg py-2 text-sm font-medium transition-colors"
          >
            {loading ? 'Adding...' : 'Add Wallet'}
          </button>

        </div>
      </div>
    </div>
  );
}