import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow requests from any host (required for port 3000 preview access)
  allowedDevOrigins: ["*"],
};

export default nextConfig;
