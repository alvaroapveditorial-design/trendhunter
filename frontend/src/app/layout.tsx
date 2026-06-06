import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Trend Hunter",
  description: "Trend detection dashboard for early opportunity discovery.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
