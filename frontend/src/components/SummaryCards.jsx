import { ArrowDownCircle, ArrowUpCircle, Activity, CheckCircle } from 'lucide-react';

const Card = ({ title, value, subtitle, icon: Icon, color }) => (
  <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
    <div className="flex justify-between items-start">
      <div>
        <p className="text-slate-400 text-sm">{title}</p>
        <p className={`text-2xl font-bold mt-1 ${color}`}>{value}</p>
        {subtitle && <p className="text-slate-500 text-xs mt-1">{subtitle}</p>}
      </div>
      <div className={`p-2 rounded-lg bg-slate-700`}>
        <Icon size={20} className={color} />
      </div>
    </div>
  </div>
);

export default function SummaryCards({ summary }) {
  if (!summary) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <Card
        title    = "Total Transactions"
        value    = {summary.total_transactions}
        icon     = {Activity}
        color    = "text-blue-400"
      />
      <Card
        title    = "Total IN"
        value    = {`${summary.total_in_matic.toFixed(4)} MATIC`}
        icon     = {ArrowDownCircle}
        color    = "text-green-400"
      />
      <Card
        title    = "Total OUT"
        value    = {`${summary.total_out_matic.toFixed(4)} MATIC`}
        icon     = {ArrowUpCircle}
        color    = "text-red-400"
      />
      <Card
        title    = "Success Rate"
        value    = {`${((summary.successful_txs / summary.total_transactions) * 100).toFixed(1)}%`}
        subtitle = {`${summary.failed_txs} failed`}
        icon     = {CheckCircle}
        color    = "text-emerald-400"
      />
    </div>
  );
}