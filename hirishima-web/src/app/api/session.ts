'use server'

import { getIronSession, SessionOptions } from "iron-session";
import { cookies } from "next/headers";

interface SessionData {
    access_token?: string;
    refresh_token?: string;
}

const session_config: SessionOptions = {
    password: process.env.SESSION_PASSWORD!,
    cookieName: process.env.SESSION_COOKIE_NAME!,
    cookieOptions: {
        secure: process.env.NODE_ENV === "production",
    },
}

export async function getSession() {
    const session = await getIronSession<SessionData>(await cookies(), session_config)
    return session
}