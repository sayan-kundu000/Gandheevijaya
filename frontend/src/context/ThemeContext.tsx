import React, { createContext, useContext, useState, useEffect } from "react";

export type ThemeMode = "dark" | "light" | "pink-neon" | "blue-neon" | "supernatural";

export interface ThemeConfig {
  id: ThemeMode;
  name: string;
  icon: string;
  description: string;
}

export const THEME_CONFIGS: ThemeConfig[] = [
  { id: "dark", name: "Dark Mode", icon: "🌙", description: "Sleek dark slate theme" },
  { id: "light", name: "Light Mode", icon: "☀️", description: "Crisp clean bright theme" },
  { id: "pink-neon", name: "Pink Neon (Girls)", icon: "💖", description: "Cyber-pink magenta glowing theme" },
  { id: "blue-neon", name: "Blue Neon (Boys)", icon: "⚡", description: "Electric cyan cyber tech theme" },
  { id: "supernatural", name: "Supernatural Mode", icon: "🔯", description: "Occult dark mystery hunter aesthetic" },
];

interface ThemeContextType {
  theme: ThemeMode;
  setTheme: (theme: ThemeMode) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setThemeState] = useState<ThemeMode>(() => {
    const saved = localStorage.getItem("app-theme") as ThemeMode;
    if (saved && ["dark", "light", "pink-neon", "blue-neon", "supernatural"].includes(saved)) {
      return saved;
    }
    return "dark";
  });

  const setTheme = (newTheme: ThemeMode) => {
    setThemeState(newTheme);
    localStorage.setItem("app-theme", newTheme);
  };

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};
