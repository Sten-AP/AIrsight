"use client";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../globals.css";
import Nav from "../components/navigation/nav";
import { Suspense } from "react";
import { QueryClient, QueryClientProvider } from "react-query";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient()
  return (
    <QueryClientProvider client={queryClient}>
    <html lang='en' className='h-full'>
      <body className='h-full bg-tremor-background-subtle'>
        <Suspense>
          <Nav />
        </Suspense>
        <main className='p-4 md:p-10 mx-auto max-w-8xl'>{children}</main>
      </body>
    </html>
    </QueryClientProvider>
  );
}
