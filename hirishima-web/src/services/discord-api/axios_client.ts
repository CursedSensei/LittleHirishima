'use server'

import axios from "axios";

const axiosDiscord = axios.create({
  baseURL: process.env.DISCORD_API_URL,
  withCredentials: true,
});

export default axiosDiscord;