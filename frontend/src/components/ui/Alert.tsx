import React from 'react';
import { AlertCircle, CheckCircle, Info, AlertTriangle } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export interface AlertProps {
  variant?: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  children: React.ReactNode;
  className?: string;
}

export const Alert: React.FC<AlertProps> = ({
  variant = 'info',
  title,
  children,
  className,
}) => {
  const configs = {
    info: {
      icon: Info,
      wrapper: 'bg-cyan-surface border-cyan-border text-navy-800',
      iconColor: 'text-primary',
    },
    success: {
      icon: CheckCircle,
      wrapper: 'bg-success-surface border-success-border text-success',
      iconColor: 'text-success',
    },
    warning: {
      icon: AlertTriangle,
      wrapper: 'bg-review-surface border-review-border text-review',
      iconColor: 'text-review',
    },
    error: {
      icon: AlertCircle,
      wrapper: 'bg-error-surface border-error-border text-error',
      iconColor: 'text-error',
    },
  };

  const { icon: Icon, wrapper, iconColor } = configs[variant];

  return (
    <div
      role="alert"
      className={twMerge(
        clsx(
          'p-4 rounded-card border flex items-start gap-3 text-sm leading-relaxed',
          wrapper,
          className
        )
      )}
    >
      <Icon className={`w-5 h-5 flex-shrink-0 mt-0.5 ${iconColor}`} />
      <div className="flex-1">
        {title && <h4 className="font-semibold mb-0.5">{title}</h4>}
        <div className="text-xs sm:text-sm">{children}</div>
      </div>
    </div>
  );
};
