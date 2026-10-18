import "./globals.css";
import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "Viloyatga Boramiz",
  description: "O‘zbekiston bo‘ylab viloyatlararo safar toping yoki safar e’lon qiling."
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="uz"><body>{children}</body></html>;
}
