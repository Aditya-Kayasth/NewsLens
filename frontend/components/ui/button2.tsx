interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: "default" | "ghost";
    size?: "sm" | "md" | "lg";
  }
  
  export const Button2: React.FC<ButtonProps> = ({ variant = "default", size = "md", ...props }) => {
    const sizeClasses = {
      sm: "px-2 py-1 text-sm",
      md: "px-4 py-2 text-base",
      lg: "px-6 py-3 text-lg",
    };
  
    return (
      <button
        className={` ${sizeClasses[size]} ${variant === "ghost" ? "bg-transparent text-white" : "bg-blue-500 text-white"}`}
        {...props}
      />
    );
  };
  