import Link from "next/link";
import { Facebook, Instagram, Linkedin } from "lucide-react";
import { Button2 } from "../../components/ui/button2";

export default function TopNav() {
  // Get current date in India Standard Time (IST)
  const dateData = new Date().toLocaleDateString("en-IN", {
    weekday: "long",  // e.g., Monday
    day: "2-digit",   // 23
    month: "long",    // February
    year: "numeric",  // 2025
  });

  return (
    <div className="bg-[#1A1D1F] border-b border-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-10">
          <div className="flex items-center gap-4">
            <Link href="https://www.facebook.com" target="_blank" className="text-gray-400 hover:text-white">
              <Facebook className="h-4 w-4" />
            </Link>
            <Link href="https://www.instagram.com" target="_blank" className="text-gray-400 hover:text-white">
              <Instagram className="h-4 w-4" />
            </Link>
            <Link href="https://www.linkedin.com" target="_blank" className="text-gray-400 hover:text-white">
              <Linkedin className="h-4 w-4" />
            </Link>
          </div>

          <div className="bg-[#0EA6E9] px-4 py-1 rounded-full">{dateData}</div>

          <div className="flex items-center gap-4 text-sm">
            <Link href="/signup">
              <Button2 variant="ghost" size="sm">
                Sign up
              </Button2>
            </Link>
            <Link href="/signin">
              <Button2 variant="ghost" size="sm">
                Sign in
              </Button2>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
