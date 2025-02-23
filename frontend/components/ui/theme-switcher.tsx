"use client";

import { useEffect, useState } from "react";
import { Sun, Moon } from "lucide-react";
import { Button2 } from "./button2";

export default function ThemeSwitcher() {
  const [theme, setTheme] = useState("dark");

  useEffect(() => {
    const storedTheme = localStorage.getItem("theme") || 
      (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    setTheme(storedTheme);
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <Button2 
      variant="ghost" 
      onClick={() => setTheme(prev => prev === "dark" ? "light" : "dark")}
    >
      {theme === "dark" ? (
        <Sun className="h-5 w-5 text-white" /> // Sun icon for dark mode
      ) : (
        <Moon className="h-5 w-5 text-black" /> // Moon icon for light mode
      )}
    </Button2>
  );
}