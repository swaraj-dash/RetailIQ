import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'highlight' | 'subtle';
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  variant = 'default',
  ...props
}) => {
  const baseStyles = 'bg-surface border rounded-card shadow-card overflow-hidden transition-all';
  
  const variants = {
    default: 'border-border',
    highlight: 'border-primary ring-1 ring-primary/20',
    subtle: 'border-border/60 bg-slate-50/50',
  };

  return (
    <div className={twMerge(clsx(baseStyles, variants[variant], className))} {...props}>
      {children}
    </div>
  );
};
