import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

import Sidebar from "../Components/Sidebar/Sidebar";
import Footer from "@/Components/Footer/footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Keyden - Password Manager",
  description: "Password Manager made by Federico Grimaldi",
  icons: {
    icon: "/favicon.ico",
  },
  openGraph: {
    title: "Keyden - Password Manager",
    description: "Password Manager made by Federico Grimaldi",
    images: [
      {
        url: "/PasswordManagerLogo.png",
        alt: "Keyden - Password Manager",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased flex flex-col min-h-screen`}>
        <div className="flex flex-1">
          <Sidebar />
          <main className="flex-1">{children}</main>
        </div>
        <Footer />
      </body>
    </html>
  );
}
