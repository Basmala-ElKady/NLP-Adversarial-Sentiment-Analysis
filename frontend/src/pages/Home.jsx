import React from 'react';
import { motion } from 'framer-motion';
import SentimentForm from '../components/SentimentForm';

const Home = () => {
    return (
        <div className="min-h-screen bg-[#0a0b1e] text-white selection:bg-blue-500/30">
            {/* Background Gradients */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full" />
                <div className="absolute top-[20%] -right-[5%] w-[30%] h-[30%] bg-indigo-600/10 blur-[100px] rounded-full" />
            </div>

            <main className="relative z-10 container mx-auto px-6 py-20">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center mb-16"
                >
                    <h1 className="text-6xl md:text-7xl font-black mb-6 bg-gradient-to-b from-white to-gray-500 bg-clip-text text-transparent">
                        Robust AI Analysis
                    </h1>
                    <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                        Evaluating sentiment with adversarial robustness. Our model is trained to resist common perturbations like typos and leetspeak.
                    </p>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.2, duration: 0.8 }}
                >
                    <SentimentForm />
                </motion.div>

                <section className="mt-32 grid md:grid-cols-3 gap-8">
                    {[
                        { title: 'Adversarial Defense', desc: 'Resistant to intentional character swaps and noise.' },
                        { title: 'DistilBERT Core', desc: 'Lightweight yet powerful transformer architecture.' },
                        { title: 'Real-time API', desc: 'Fast inference speeds via optimized FastAPI backend.' }
                    ].map((feature, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.4 + (i * 0.1) }}
                            className="p-8 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors"
                        >
                            <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                            <p className="text-gray-400 leading-relaxed">{feature.desc}</p>
                        </motion.div>
                    ))}
                </section>
            </main>

            <footer className="relative z-10 py-10 border-t border-white/5 text-center text-gray-500 text-sm">
                &copy; 2024 Robust NLP Analysis Project. All rights reserved.
            </footer>
        </div>
    );
};

export default Home;
