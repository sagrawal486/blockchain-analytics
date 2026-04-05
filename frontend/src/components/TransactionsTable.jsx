import { ExternalLink, CheckCircle, XCircle } from 'lucide-react';

const shortHash = (hash) => hash ? `${hash.slice(0,8)}...${hash.slice(-6)}` : '-';
const shortAddr = (addr) => addr ? `${addr.slice(0,6)}...${addr.slice(-4)}` : '-';
const formatDate = (dt)  => dt ? new Date(dt).toLocaleString('en-IN') : '-';

export default function TransactionsTable({ transactions }) {
  if (!transactions?.length) return (
    <div className="bg-slate-800 rounded-xl p-8 text-center text-slate-400">
      No transactions found
    </div>
  );

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-700 text-slate-400 text-xs uppercase">
              <th className="text-left p-4">Status</th>
              <th className="text-left p-4">Tx Hash</th>
              <th className="text-left p-4">Date</th>
              <th className="text-left p-4">From</th>
              <th className="text-left p-4">To</th>
              <th className="text-right p-4">Value (MATIC)</th>
              <th className="text-right p-4">Fee (MATIC)</th>
              <th className="text-center p-4">Explorer</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx, i) => (
              <tr 
                key={tx.tx_hash} 
                className={`border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors
                  ${i % 2 === 0 ? 'bg-slate-800' : 'bg-slate-800/50'}`}
              >
                <td className="p-4">
                  {tx.successful 
                    ? <CheckCircle size={16} className="text-green-400" />
                    : <XCircle    size={16} className="text-red-400" />
                  }
                </td>
                <td className="p-4 font-mono text-blue-400">
                  {shortHash(tx.tx_hash)}
                </td>
                <td className="p-4 text-slate-400">
                  {formatDate(tx.block_signed_at)}
                </td>
                <td className="p-4 font-mono text-slate-300">
                  {shortAddr(tx.from_address)}
                </td>
                <td className="p-4 font-mono text-slate-300">
                  {shortAddr(tx.to_address)}
                </td>
                <td className="p-4 text-right font-mono text-emerald-400">
                  {tx.value_native ? parseFloat(tx.value_native).toFixed(6) : '0'}
                </td>
                <td className="p-4 text-right font-mono text-slate-400 text-xs">
                  {tx.fees_paid ? parseFloat(tx.fees_paid).toFixed(6) : '0'}
                </td>
               <td className="p-4 text-center">
                  <a href={`https://polygonscan.com/tx/${tx.tx_hash}`} target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-blue-400 transition-colors">
                    <ExternalLink size={14} />
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}