// Error Boundary Component for StadiumVerse Intelligence OS
import React from 'react';
import { motion } from 'framer-motion';

interface ErrorBoundaryProps {
  children: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('StadiumVerse Intelligence OS Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-stadium-dark via-stadium-darker to-stadium-accent flex items-center justify-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-8 text-center max-w-md mx-4"
          >
            <div className="text-6xl mb-4">🧠</div>
            
            <h2 className="text-2xl font-bold text-white mb-4">
              StadiumVerse Intelligence OS Error
            </h2>
            
            <p className="text-gray-300 mb-6">
              The Living Brain encountered an unexpected error. Please refresh the page or contact support.
            </p>
            
            {this.state.error && (
              <details className="text-left mb-6">
                <summary className="text-sm text-gray-400 cursor-pointer hover:text-white">
                  Error Details
                </summary>
                <pre className="text-xs text-red-400 mt-2 p-2 bg-black bg-opacity-30 rounded overflow-x-auto">
                  {this.state.error.toString()}
                </pre>
              </details>
            )}
            
            <div className="space-y-3">
              <button
                onClick={() => window.location.reload()}
                className="w-full btn-fifa-primary"
              >
                Refresh Application
              </button>
              
              <button
                onClick={() => this.setState({ hasError: false })}
                className="w-full btn-fifa-secondary"
              >
                Try Again
              </button>
            </div>
          </motion.div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
