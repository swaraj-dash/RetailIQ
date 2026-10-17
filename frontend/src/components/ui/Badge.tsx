import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'cyan' | 'navy';
  size?: 'sm' | 'md';
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  className,
  variant = 'default',
  size = 'md',
  ...props
}) => {
  const baseStyles = 'inline-flex items-center gap-1.5 font-medium rounded-full select-none';

  const variants = {
    default: 'bg-slate-100 text-text-secondary border border-slate-200',
    success: 'bg-success-surface text-success border border-success-border',
    warning: 'bg-review-surface text-review border border-review-border',
    error: 'bg-error-surface text-error border border-error-border',
    cyan: 'bg-cyan-surface text-navy-800 border border-cyan-border',
    navy: 'bg-navy-800 text-white border border-navy-700',
  };

  const sizes = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-xs px-2.5 py-1',
  };

  return (
    <span className={twMerge(clsx(baseStyles, variants[variant], sizes[size], className))} {...props}>
      {children}
    </span>
  );
};
