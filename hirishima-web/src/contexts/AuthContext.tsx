'use client'

import React from "react";

interface AuthContextType {
    isAuthenticated: boolean;
    authenticating: boolean;
    username: string;
    login: (code: string) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = React.createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [isAuthenticated, setIsAuthenticated] = React.useState(false);
    const [username, setUsername] = React.useState<string>('');
    const [authenticating, setAuthenticating] = React.useState(false);

    async function login(code: string) {
        if (authenticating) return;

        // Implement login logic here
    }

    async function logout() {
        // Implement logout logic here
    }

    return (
        <AuthContext.Provider value={{ isAuthenticated, authenticating, username, login, logout }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = React.useContext(AuthContext);

    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }

    return context;
}