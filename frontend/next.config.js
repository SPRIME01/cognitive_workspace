/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  eslint: {
    dirs: ['src']
  },
  images: {
    domains: ['localhost']
  },
  experimental: {
    outputFileTracingRoot: __dirname,
  },
  webpack: (config) => {
    // Custom webpack configurations if needed
    return config;
  },
}

module.exports = nextConfig
