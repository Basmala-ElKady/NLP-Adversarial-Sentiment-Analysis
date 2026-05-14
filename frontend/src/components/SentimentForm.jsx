import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Shield, Zap, RefreshCw } from 'lucide-react';
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
            setError('Failed to get prediction. Make sure the backend is running.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-6 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 shadow-2xl">
            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="relative">
                    <label htmlFor="sentiment-input" className="block text-sm font-medium text-blue-200 mb-2">
                        Enter text to analyze
                    </label>
                    <textarea
                        id="sentiment-input"
                        rows="4"
                        className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-white placeholder-gray-500"
                        placeholder="e.g., This movie is absolutely stunning, a masterpiece of modern cinema!"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                    />
                </div>

                <div className="flex items-center justify-between">
                    <button
                        type="submit"
                        disabled={loading || !text.trim()}
                        className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all ${
                            loading || !text.trim()
                                ? 'bg-gray-600 cursor-not-allowed'
                                : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:scale-105 active:scale-95 shadow-lg shadow-blue-500/30'
                        }`}
                    >
                        {loading ? (
                            <RefreshCw className="animate-spin w-5 h-5" />
                        ) : (
                            <Send className="w-5 h-5" />
                        )}
                        {loading ? 'Analyzing...' : 'Analyze Sentiment'}
                    </button>

                    <div className="flex gap-4">
                        <div className="flex items-center gap-1 text-xs text-blue-300">
                            <Shield className="w-4 h-4" />
                            <span>Robust Model</span>
                        </div>
                        <div className="flex items-center gap-1 text-xs text-indigo-300">
                            <Zap className="w-4 h-4" />
                            <span>Fast Inference</span>
                        </div>
                    </div>
                </div>
            </form>

            <AnimatePresence>
                {result && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="mt-8 p-6 rounded-xl border border-white/10 bg-white/5"
                    >
                        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Analysis Result</h3>
                        <div className="flex items-center justify-between">
                            <span className="text-3xl font-black text-white">
                                {result}
                            </span>
                            <div className={`px-4 py-1 rounded-full text-xs font-bold ${
                                result === 'Positive' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                            }`}>
                                Confidence High
                            </div>
                        </div>
                    </motion.div>
                )}

                {error && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm"
                    >
                        {error}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default SentimentForm;
