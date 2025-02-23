import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  variant?: "default" | "outlined"; // Custom variant
}

export const Input2: React.FC<InputProps> = ({ variant = "default", className, ...props }) => {
  return (
    <input
      className={`border rounded-md p-2 focus:ring-2 focus:ring-[#0EA6E9] outline-none ${
        variant === "outlined" ? "border-gray-500 bg-transparent" : "border-gray-300 bg-white"
      } ${className}`}
      {...props}
    />
  );
};
