import React from 'react';
import { motion } from 'framer-motion';

interface Props {
  title: string;
  icon: string;
  color: string;
  description: string;
}

export const PlaceholderPage: React.FC<Props> = ({ title, icon, color, description }) => (
  <div className="h-full flex flex-col items-center justify-center p-8">
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: 'spring', stiffness: 200 }}
      className="text-center"
    >
      <motion.div
        className="text-7xl mb-6"
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
      >
        {icon}
      </motion.div>
      <h1
        className="text-4xl font-light mb-3"
        style={{ color: color, letterSpacing: '-0.02em' }}
      >
        {title}
      </h1>
      <p className="text-sm max-w-sm" style={{ color: '#64748B' }}>{description}</p>
      <div className="mt-8 flex items-center justify-center gap-2">
        <motion.div
          className="w-2 h-2 rounded-full"
          style={{ background: color }}
          animate={{ scale: [1, 1.4, 1] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        />
        <span className="text-xs font-medium" style={{ color }}>LOADING INTELLIGENCE DATA...</span>
      </div>
    </motion.div>
  </div>
);
