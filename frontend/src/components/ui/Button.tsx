import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger' | 'ghost' | 'success';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  className,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-input transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 disabled:cursor-not-allowed select-none min-h-[44px]';

  const variants = {
    primary: 'bg-primary text-white hover:bg-primary-hover focus-visible:outline-primary active:scale-[0.99]',
    secondary: 'bg-navy-800 text-white hover:bg-navy-900 focus-visible:outline-navy-800',
    outline: 'border border-border bg-white text-text-primary hover:bg-slate-50 focus-visible:outline-primary',
    danger: 'bg-error text-white hover:bg-red-800 focus-visible:outline-error',
    ghost: 'text-text-secondary hover:text-text-primary hover:bg-slate-100 focus-visible:outline-primary',
    success: 'bg-success text-white hover:bg-green-800 focus-visible:outline-success',
  };

  const sizes = {
    sm: 'text-xs px-3 py-1.5 min-h-[36px]',
    md: 'text-sm px-4 py-2 min-h-[44px]',
    lg: 'text-base px-6 py-2.5 min-h-[48px]',
  };

  return (
    <button
      className={twMerge(clsx(baseStyles, variants[variant], sizes[size], className))}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="flex items-center gap-2">
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{children}</span>
        </span>
      ) : (
        children
      )}
    </button>
  );
};
