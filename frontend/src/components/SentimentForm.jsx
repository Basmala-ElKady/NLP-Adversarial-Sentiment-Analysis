import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, CheckCircle2, AlertCircle, Loader2, Sparkles } from 'lucide-react';
import { predictSentiment } from '../services/api';

const SentimentForm = () => {
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!text.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await predictSentiment(text);
            setResult(data.prediction);
        } catch (err) {
            setError('System offline. Please ensure the backend engine is running.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto">
            <div className="glass p-1 rounded-[2.5rem]">
                <div className="bg-[#11122d]/50 rounded-[2.25rem] p-8 md:p-12">
                    <form onSubmit={handleSubmit} className="space-y-8">
                        <div className="relative group">
                            <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl blur opacity-20 group-focus-within:opacity-40 transition duration-500"></div>
                            <textarea
                                id="sentiment-input"
                                rows="5"
                                className="relative w-full px-6 py-5 bg-[#0a0b1e] border border-white/10 rounded-2xl focus:ring-1 focus:ring-indigo-500 outline-none transition-all text-lg text-white placeholder-gray-600"
                                placeholder="Drop your text here for analysis..."
                                value={text}
                                onChange={(e) => setText(e.target.value)}
                            />
                        </div>

                        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                            <div className="flex items-center gap-4 text-gray-400 text-sm">
                                <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 border border-white/10">
                                    <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                                    <span>Real-time Inference</span>
                                </div>
                                <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 border border-white/10">
                                    <CheckCircle2 className="w-3.5 h-3.5 text-green-400" />
                                    <span>Robust Model</span>
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={loading || !text.trim()}
                                className={`group relative flex items-center gap-3 px-10 py-4 rounded-2xl font-bold text-lg transition-all overflow-hidden ${
                                    loading || !text.trim()
                                        ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
                                        : 'bg-indigo-600 text-white hover:scale-105 active:scale-95 shadow-2xl shadow-indigo-600/40'
                                }`}
                            >
                                {loading ? (
                                    <Loader2 className="animate-spin w-5 h-5" />
                                ) : (
                                    <Send className="w-5 h-5 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                                )}
                                <span>{loading ? 'Processing...' : 'Analyze Now'}</span>
                                {!loading && text.trim() && (
                                    <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity" />
                                )}
                            </button>
                        </div>
                    </form>

                    <AnimatePresence>
                        {result && (
                            <motion.div
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="mt-12 p-8 rounded-3xl bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10"
                            >
                                <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                                    <div>
                                        <p className="text-xs font-bold text-indigo-400 uppercase tracking-[0.2em] mb-3">Model Prediction</p>
                                        <h3 className={`text-5xl font-black ${
                                            result === 'Positive' ? 'text-green-400' : 'text-red-400'
                                        }`}>
                                            {result}
                                        </h3>
                                    </div>
                                    <div className="flex flex-col items-end">
                                        <div className="text-sm text-gray-500 mb-2">Robustness Score</div>
                                        <div className="flex gap-1">
                                            {[1, 2, 3, 4, 5].map((s) => (
                                                <div key={s} className="w-8 h-1.5 rounded-full bg-indigo-500" />
                                            ))}
                                        </div>
                                        <span className="text-xs text-indigo-400 mt-2 font-bold uppercase">Optimal Defense</span>
                                    </div>
                                </div>
                            </motion.div>
                        )}

                        {error && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="mt-8 p-5 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400 flex items-center gap-3 text-sm"
                            >
                                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                                <span>{error}</span>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
};

export default SentimentForm;
