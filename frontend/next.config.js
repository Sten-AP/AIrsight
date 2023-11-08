/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        domains: ['avatars.githubusercontent.com', 'avatar.vercel.sh']
      },
    output: 'standalone',
}

module.exports = nextConfig
