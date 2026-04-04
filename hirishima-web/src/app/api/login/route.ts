'use server'

import { NextRequest } from "next/server";
import { getSession } from "../session";

export async function GET(request: NextRequest) {
    const code = request.nextUrl.searchParams.get("code");

    if (!code) {
        return new Response("Missing code parameter", {
            status: 400,
        });
    }

    const session = await getSession();

    await session.save();

    return new Response("Hello, world!", {
        status: 200,
    });
}