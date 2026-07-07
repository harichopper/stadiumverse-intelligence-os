// Command Center Component for StadiumVerse Intelligence OS
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  CpuChipIcon,
  CommandLineIcon,
  BoltIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline';

const CommandCenter: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [commands, setCommands] = useState<string[]>([]);

  useEffect(() => {
    // Simulate loading
    setTimeout(() => setIsLoading(false), 1000);
  }, []);

  const executeCommand = (command: string) => {
    setCommands(prev => [...prev, `> ${command}`, `Command executed: ${command}`]);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-card p-8 text-center"
        >
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <h2 className="text-xl font-bold text-white mb-2">🎮 Loading Command Center</h2>
          <p className="text-gray-300">Initializing advanced controls...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-stadium-dark via-stadium-darker to-stadium-accent p-6">
      {/* Header */}
      <motion.header
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="glass-card p-4 mb-6"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <CommandLineIcon className="w-8 h-8 text-green-400" />
            <div>
              <h1 className="text-2xl font-bold text-white">Command Center</h1>
              <p className="text-gray-300">Advanced AI Control Interface</p>
            </div>
          </div>
          
          <button
            onClick={() => window.history.back()}
            className="btn-fifa-secondary"
          >
            ← Back to Dashboard
          </button>
        </div>
      </motion.header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Command Panel */}
        <motion.div
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="glass-card p-6"
        >
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <BoltIcon className="w-6 h-6 text-yellow-400 mr-2" />
            Quick Commands
          </h2>
          
          <div className="space-y-3">
            <button
              onClick={() => executeCommand('AI_STATUS_CHECK')}
              className="w-full btn-fifa-primary text-left"
            >
              🤖 Check AI Status
            </button>
            
            <button
              onClick={() => executeCommand('SIMULATE_CROWD')}
              className="w-full btn-fifa-primary text-left"
            >
              👥 Simulate Crowd Dynamics
            </button>
            
            <button
              onClick={() => executeCommand('ANALYZE_PATTERNS')}
              className="w-full btn-fifa-primary text-left"
            >
              📊 Analyze Behavioral Patterns
            </button>
            
            <button
              onClick={() => executeCommand('GENERATE_REPORT')}
              className="w-full btn-fifa-primary text-left"
            >
              📋 Generate Intelligence Report
            </button>
          </div>
        </motion.div>

        {/* System Information */}
        <motion.div
          initial={{ x: 100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="glass-card p-6"
        >
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <CpuChipIcon className="w-6 h-6 text-blue-400 mr-2" />
            System Status
          </h2>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-300">AI Engine</span>
              <span className="px-3 py-1 bg-green-500 bg-opacity-20 text-green-400 rounded-full text-sm">
                OPERATIONAL
              </span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Database</span>
              <span className="px-3 py-1 bg-green-500 bg-opacity-20 text-green-400 rounded-full text-sm">
                CONNECTED
              </span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-300">WebSocket</span>
              <span className="px-3 py-1 bg-yellow-500 bg-opacity-20 text-yellow-400 rounded-full text-sm">
                SIMULATED
              </span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Memory Usage</span>
              <span className="text-white">2.1GB / 8GB</span>
            </div>
          </div>
        </motion.div>

        {/* Command Terminal */}
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="lg:col-span-2 glass-card p-6"
        >
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <CommandLineIcon className="w-6 h-6 text-green-400 mr-2" />
            Command Terminal
          </h2>
          
          <div className="bg-black bg-opacity-50 rounded-lg p-4 h-64 overflow-y-auto font-mono text-sm">
            <div className="text-green-400 mb-2">StadiumVerse Intelligence OS Command Terminal</div>
            <div className="text-gray-400 mb-4">Type commands above or use quick actions</div>
            
            {commands.map((cmd, index) => (
              <div
                key={index}
                className={`mb-1 ${
                  cmd.startsWith('>') ? 'text-yellow-400' : 'text-gray-300'
                }`}
              >
                {cmd}
              </div>
            ))}
            
            {commands.length === 0 && (
              <div className="text-gray-500 italic">
                No commands executed yet. Use the quick commands above.
              </div>
            )}
          </div>
        </motion.div>
      </div>

      {/* Warning Notice */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="glass-card p-4 mt-6 border-yellow-500 border-opacity-30"
      >
        <div className="flex items-center space-x-2 text-yellow-400">
          <ExclamationTriangleIcon className="w-5 h-5" />
          <span className="font-semibold">Development Mode</span>
        </div>
        <p className="text-gray-300 text-sm mt-2">
          This Command Center is in development mode. Advanced controls and real-time command execution will be available in production deployment.
        </p>
      </motion.div>
    </div>
  );
};

export default CommandCenter;
