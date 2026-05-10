import "./globals.css";

export const metadata = {
  title: "F.R.I.D.A.Y AI OS",
  description: "Fully Responsive Intelligent Digital Assistant for You",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}