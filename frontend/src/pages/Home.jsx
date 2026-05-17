import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Brain, Zap, Terminal } from 'lucide-react';
import SentimentForm from '../components/SentimentForm';
import AdversarialLab from '../components/AdversarialLab';

const Home = () => {
    return (
        <div className="min-h-screen bg-[#0a0b1e] text-white selection:bg-indigo-500/30 pb-20">
            {/* Ambient Background Elements */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-indigo-600/10 blur-[150px] rounded-full animate-float" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/10 blur-[120px] rounded-full animate-float" style={{ animationDelay: '-2s' }} />
                <div className="absolute top-[20%] right-[10%] w-[30%] h-[30%] bg-blue-600/5 blur-[100px] rounded-full" />
            </div>

            {/* Navigation / Header */}
            <header className="relative z-10 container mx-auto px-6 py-8 flex justify-between items-center">
                <div className="flex items-center gap-2 group cursor-pointer">
                    <div className="w-10 h-10 gradient-primary rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-110 transition-transform">
                        <Shield className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-xl font-black tracking-tighter">ROBUST.AI</span>
                </div>
                <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
                    <a href="#" className="hover:text-white transition-colors">Documentation</a>
                    <a href="#" className="hover:text-white transition-colors">Benchmarks</a>
                    <a href="#" className="px-5 py-2 glass rounded-full hover:bg-white/10 transition-colors">GitHub</a>
                </div>
            </header>

            <main className="relative z-10 container mx-auto px-6 pt-16">
                {/* Hero Section */}
                <div className="max-w-4xl mx-auto text-center mb-24">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-bold text-indigo-400 mb-6"
                    >
                        <Terminal className="w-3 h-3" />
                        <span>POWERED BY DISTILBERT & TEXTATTACK</span>
                    </motion.div>
                    
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        className="text-6xl md:text-8xl font-black mb-8 leading-[1.1] tracking-tight"
                    >
                        Next-Gen <span className="gradient-text">Sentiment</span> <br />
                        <span className="text-indigo-500">Robustness.</span>
                    </motion.h1>
                    
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2, duration: 0.8 }}
                        className="text-xl text-gray-400 leading-relaxed max-w-2xl mx-auto"
                    >
                        A deep learning system designed to survive adversarial noise, 
                        char-level perturbations, and semantic shifts. 
                        Testing the boundaries of NLP security.
                    </motion.p>
                </div>

                {/* Analysis Section */}
                <div className="grid lg:grid-cols-1 gap-20">
                    <motion.div
                        initial={{ opacity: 0, y: 40 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 1 }}
                    >
                        <SentimentForm />
                    </motion.div>

                    {/* Adversarial Lab Section */}
                    <AdversarialLab />
                </div>

                {/* Features Grid */}
                <section className="mt-40 grid md:grid-cols-3 gap-8">
                    {[
                        { 
                            icon: <Shield className="w-6 h-6 text-indigo-400" />,
                            title: 'Defense Pipeline', 
                            desc: 'Multi-stage defense mechanisms including adversarial training and input sanitization.' 
                        },
                        { 
                            icon: <Brain className="w-6 h-6 text-purple-400" />,
                            title: 'DistilBERT Core', 
                            desc: 'Leveraging state-of-the-art transformer architecture optimized for edge inference.' 
                        },
                        { 
                            icon: <Zap className="w-6 h-6 text-yellow-400" />,
                            title: 'Low Latency', 
                            desc: 'Response times under 100ms for real-time analysis through our FastAPI backbone.' 
                        }
                    ].map((feature, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: i * 0.2 }}
                            className="glass p-10 rounded-3xl group hover:border-indigo-500/50 transition-all duration-500"
                        >
                            <div className="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-500">
                                {feature.icon}
                            </div>
                            <h3 className="text-2xl font-bold mb-4">{feature.title}</h3>
                            <p className="text-gray-400 leading-relaxed">{feature.desc}</p>
                        </motion.div>
                    ))}
                </section>
            </main>

            <footer className="mt-40 pt-10 border-t border-white/5 text-center">
                <div className="container mx-auto px-6">
                    <p className="text-gray-500 text-sm">
                        &copy; 2024 Robust Sentiment Analysis Project. Built for NLP Security Research.
                    </p>
                </div>
            </footer>
        </div>
    );
};

export default Home;
