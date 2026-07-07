// Login Component for StadiumVerse AI V2
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CpuChipIcon, ShieldCheckIcon, GlobeAltIcon } from '@heroicons/react/24/outline';

const Login: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {
    setIsLoading(true);
    
    // Simulate login process
    setTimeout(() => {
      // For demo purposes, redirect to dashboard
      window.location.href = '/';
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-stadium-dark via-stadium-darker to-stadium-accent flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.9 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="glass-card p-8 w-full max-w-md mx-4"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="text-6xl mb-4"
          >
            🧠
          </motion.div>
          
          <h1 className="text-3xl font-bold text-white mb-2">
            StadiumVerse AI V2
          </h1>
          <p className="text-gray-300 text-lg">
            "The Living Brain of the Stadium"
          </p>
        </div>

        {/* Features */}
        <div className="space-y-4 mb-8">
          <motion.div
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="flex items-center space-x-3 text-gray-300"
          >
            <CpuChipIcon className="w-6 h-6 text-blue-400" />
            <span>Local AI Processing (Ollama)</span>
          </motion.div>
          
          <motion.div
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="flex items-center space-x-3 text-gray-300"
          >
            <ShieldCheckIcon className="w-6 h-6 text-green-400" />
            <span>Completely Offline Operation</span>
          </motion.div>
          
          <motion.div
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="flex items-center space-x-3 text-gray-300"
          >
            <GlobeAltIcon className="w-6 h-6 text-purple-400" />
            <span>FIFA World Cup 2026 Ready</span>
          </motion.div>
        </div>

        {/* Login Button */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.6 }}
        >
          <button
            onClick={handleLogin}
            disabled={isLoading}
            className="w-full btn-fifa-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                <span>Connecting to Living Brain...</span>
              </>
            ) : (
              <span>Access Dashboard</span>
            )}
          </button>
        </motion.div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="text-center mt-8 text-sm text-gray-400"
        >
          <p>AI Native Stadium Intelligence Platform</p>
          <p className="mt-1">No external connections required</p>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Login;