import React, { useEffect, useRef } from 'react';

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  opacity: number;
  color: string;
}

export const AnimatedBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const animFrameRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const colors = ['#3B82F6', '#8B5CF6', '#06B6D4', '#10B981'];

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    // Init particles
    particlesRef.current = Array.from({ length: 80 }, () => ({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random() * 0.5 + 0.1,
      color: colors[Math.floor(Math.random() * colors.length)],
    }));

    let time = 0;
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      time += 0.005;

      // Draw gradient orbs
      const orbs = [
        { x: canvas.width * 0.2, y: canvas.height * 0.3, r: 300, color: 'rgba(59,130,246,0.06)' },
        { x: canvas.width * 0.8, y: canvas.height * 0.6, r: 350, color: 'rgba(139,92,246,0.05)' },
        { x: canvas.width * 0.5, y: canvas.height * 0.8, r: 250, color: 'rgba(6,182,212,0.04)' },
      ];

      orbs.forEach(orb => {
        const ox = orb.x + Math.sin(time * 0.5) * 50;
        const oy = orb.y + Math.cos(time * 0.3) * 40;
        const grad = ctx.createRadialGradient(ox, oy, 0, ox, oy, orb.r);
        grad.addColorStop(0, orb.color);
        grad.addColorStop(1, 'transparent');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(ox, oy, orb.r, 0, Math.PI * 2);
        ctx.fill();
      });

      // Draw grid
      ctx.strokeStyle = 'rgba(59,130,246,0.03)';
      ctx.lineWidth = 1;
      const gridSize = 50;
      for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }
      for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }

      // Draw particles + connections
      const particles = particlesRef.current;
      particles.forEach((p, i) => {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;

        // Connect nearby particles
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[j].x - p.x;
          const dy = particles[j].y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            ctx.strokeStyle = `rgba(59,130,246,${0.08 * (1 - dist / 120)})`;
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }

        // Draw particle
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.opacity;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
      });

      // Stadium light beams (subtle)
      const beams = [
        { x: canvas.width * 0.1, angle: 0.3 },
        { x: canvas.width * 0.9, angle: -0.3 },
      ];
      beams.forEach(beam => {
        const grad = ctx.createLinearGradient(
          beam.x, canvas.height,
          beam.x + Math.sin(beam.angle) * 400,
          canvas.height - 400
        );
        grad.addColorStop(0, 'rgba(59,130,246,0.04)');
        grad.addColorStop(1, 'transparent');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.moveTo(beam.x, canvas.height);
        ctx.lineTo(beam.x - 80 + Math.sin(time) * 20, 0);
        ctx.lineTo(beam.x + 80 + Math.sin(time) * 20, 0);
        ctx.closePath();
        ctx.fill();
      });

      animFrameRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      cancelAnimationFrame(animFrameRef.current);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none"
      style={{ zIndex: 0 }}
    />
  );
};
