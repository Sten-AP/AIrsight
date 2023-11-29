import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Nav from "./components/navigation/nav";
import { Suspense } from "react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AIrsight",
  description: "Insights in airquality data powered by AI",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang='en' className='h-full bg-gray-50'>
      <body className='h-full'>
        <Suspense>
          <Nav />
        </Suspense>
        <main className='p-4 md:p-10 mx-auto max-w-8xl'>{children}</main>
      </body>
    </html>
  );
}
