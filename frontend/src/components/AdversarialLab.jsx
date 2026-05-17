import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Skull, AlertTriangle, ChevronRight, Activity, Copy, Check } from 'lucide-react';
import { attackText } from '../services/api';

const attack_engine = [
    { id: 'textfooler', name: 'TextFooler', desc: 'Synonym substitution using word embeddings.' },
    { id: 'bae', name: 'BAE', desc: 'BERT-based Adversarial Examples.' },
    { id: 'deepwordbug', name: 'DeepWordBug', desc: 'Character-level transformations (typos).' },
    { id: 'pwws', name: 'PWWS', desc: 'Probability Weighted Word Saliency.' },
];

const AdversarialLab = () => {
    const [text, setText] = useState('');
    const [selectedAttack, setSelectedAttack] = useState(attack_engine[2].id);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [copied, setCopied] = useState(false);

    const handleAttack = async () => {
        if (!text.trim()) return;
        setLoading(true);
        setResult(null);
        try {
            const data = await attackText(text, selectedAttack);
            setResult(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = (txt) => {
        navigator.clipboard.writeText(txt);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <section className="mt-20">
            <div className="flex items-center gap-3 mb-8">
                <div className="p-2 bg-red-500/20 rounded-lg">
                    <Skull className="w-6 h-6 text-red-400" />
                </div>
                <div>
                    <h2 className="text-3xl font-bold">Adversarial Lab</h2>
                    <p className="text-gray-400">Stress test your models with automated attack_engine</p>
                </div>
            </div>

            <div className="grid lg:grid-cols-2 gap-10">
                {/* Left Side: Controls */}
                <div className="space-y-6">
                    <div className="glass p-6 rounded-2xl">
                        <label className="block text-sm font-medium text-gray-400 mb-4">Select Attack Strategy</label>
                        <div className="grid sm:grid-cols-2 gap-4">
                            {attack_engine.map((atk) => (
                                <button
                                    key={atk.id}
                                    onClick={() => setSelectedAttack(atk.id)}
                                    className={`p-4 rounded-xl border text-left transition-all ${selectedAttack === atk.id
                                            ? 'bg-red-500/10 border-red-500/50 text-red-400 shadow-lg shadow-red-500/10'
                                            : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10'
                                        }`}
                                >
                                    <div className="font-bold mb-1">{atk.name}</div>
                                    <div className="text-xs opacity-70">{atk.desc}</div>
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className="glass p-6 rounded-2xl">
                        <label className="block text-sm font-medium text-gray-400 mb-4">Input for Attack</label>
                        <textarea
                            rows="4"
                            className="w-full bg-black/20 border border-white/10 rounded-xl p-4 text-white outline-none focus:ring-2 focus:ring-red-500/50 transition-all"
                            placeholder="Enter text to perturb..."
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                        />
                        <button
                            onClick={handleAttack}
                            disabled={loading || !text.trim()}
                            className={`w-full mt-4 py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all ${loading || !text.trim()
                                    ? 'bg-gray-700 cursor-not-allowed opacity-50'
                                    : 'bg-gradient-to-r from-red-600 to-orange-600 hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-red-600/20'
                                }`}
                        >
                            {loading ? (
                                <Activity className="w-5 h-5 animate-spin" />
                            ) : (
                                <AlertTriangle className="w-5 h-5" />
                            )}
                            {loading ? 'Simulating Attack...' : 'Execute Attack'}
                        </button>
                    </div>
                </div>

                {/* Right Side: Results */}
                <div className="relative">
                    <AnimatePresence mode="wait">
                        {result ? (
                            <motion.div
                                key="result"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="glass p-8 rounded-2xl h-full border-red-500/20"
                            >
                                <div className="flex items-center justify-between mb-8">
                                    <h3 className="text-xl font-bold text-red-400">Attack Payload</h3>
                                    <button
                                        onClick={() => copyToClipboard(result.perturbed_text)}
                                        className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                                    >
                                        {copied ? <Check className="w-5 h-5 text-green-400" /> : <Copy className="w-5 h-5" />}
                                    </button>
                                </div>

                                <div className="space-y-6">
                                    <div>
                                        <div className="text-xs text-gray-500 uppercase tracking-widest mb-2 font-bold">Original</div>
                                        <div className="p-4 bg-white/5 rounded-xl border border-white/5 text-gray-400 italic">
                                            "{result.original_text}"
                                        </div>
                                    </div>

                                    <div className="flex justify-center">
                                        <ChevronRight className="w-8 h-8 text-red-500/50 rotate-90 lg:rotate-0" />
                                    </div>

                                    <div>
                                        <div className="text-xs text-red-500/70 uppercase tracking-widest mb-2 font-bold">Perturbed (Adversarial)</div>
                                        <div className="p-4 bg-red-500/5 rounded-xl border border-red-500/20 text-white font-mono text-lg">
                                            "{result.perturbed_text}"
                                        </div>
                                    </div>

                                    <div className="pt-6 border-t border-white/10">
                                        <div className="flex items-center justify-between">
                                            <span className="text-gray-400">Robust Model Prediction:</span>
                                            <span className={`px-4 py-1 rounded-full text-xs font-bold ${result.prediction === 'Positive' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                                                }`}>
                                                {result.prediction}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        ) : (
                            <motion.div
                                key="placeholder"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="glass p-8 rounded-2xl h-full flex flex-col items-center justify-center text-center border-dashed border-2 border-white/5"
                            >
                                <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-4">
                                    <Activity className="w-8 h-8 text-gray-600" />
                                </div>
                                <h3 className="text-gray-500 font-bold">Waiting for simulation...</h3>
                                <p className="text-gray-600 text-sm max-w-[200px] mt-2">Select an attack and input text to see how our robust model reacts.</p>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </section>
    );
};

export default AdversarialLab;
