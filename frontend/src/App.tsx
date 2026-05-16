import { useState } from 'react';
import { account } from './lib/appwrite';
import { Terminal, ShieldCheck, AlertCircle } from 'lucide-react';

export default function App() {
  const [pingStatus, setPingStatus] = useState<string>('Not tested yet');
  const [loading, setLoading] = useState<boolean>(false);

  const handlePing = async () => {
    setLoading(true);
    try {
      // Bypasses login checks to create a fast guest session on Appwrite Cloud
      const session = await account.createAnonymousSession();
      setPingStatus(`Success! Appwrite connected. Guest Session ID: ${session.$id}`);
    } catch (error: any) {
      setPingStatus(`Connection failed: ${error.message || error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900 text-slate-50 p-6">
      <div className="max-w-md w-full bg-slate-800 border border-slate-700 p-8 rounded-xl shadow-2xl text-center">
        <div className="flex justify-center mb-4">
          <Terminal className="w-12 h-12 text-sky-400" />
        </div>
        <h1 className="text-2xl font-bold mb-2 tracking-tight">DevSnap Custom Setup</h1>
        <p className="text-slate-400 text-sm mb-6">Testing connection to Appwrite Cloud (Frankfurt)</p>
        
        <button
          onClick={handlePing}
          disabled={loading}
          className="w-full bg-sky-500 hover:bg-sky-600 disabled:bg-slate-700 text-white font-medium py-3 px-4 rounded-lg transition-colors cursor-pointer flex items-center justify-center gap-2"
        >
          {loading ? 'Pinging...' : 'Send a Ping'}
        </button>

        <div className="mt-6 p-4 bg-slate-900 border border-slate-800 rounded-lg text-xs font-mono text-left break-all flex items-start gap-2">
          {pingStatus.includes('Success') ? (
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
          ) : pingStatus.includes('failed') ? (
            <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
          ) : null}
          <span>{pingStatus}</span>
        </div>
      </div>
    </div>
  );
}
