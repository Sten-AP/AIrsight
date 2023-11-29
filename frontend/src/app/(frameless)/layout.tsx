import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../globals.css";
import Nav from "../components/navigation/nav";
import { Suspense } from "react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AIrsight",
  description: "Insights in airquality data powered by AI",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang='en' className='h-full'>
      <body className='h-full  bg-tremor-background-subtle'>
        <Suspense>
          <Nav />
        </Suspense>
        <main className='min-w-full'>{children}</main>
      </body>
    </html>
  );
}
