import { Facebook, Instagram, Linkedin } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-gray-900 border-t border-gray-800 mt-8">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About Section */}
          <div className="space-y-4">
            <h3 className="text-[#0EA6E9] text-lg font-bold">About NewsLens</h3>
            <p className="text-gray-300">
              NewsLens is your go-to source for the latest news and updates in travel, technology, and finance. Stay informed with our in-depth coverage.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-[#0EA6E9] text-lg font-bold">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-300 hover:text-[#0EA6E9]">Home</a></li>
              <li><a href="#" className="text-gray-300 hover:text-[#0EA6E9]">Travel</a></li>
              <li><a href="#" className="text-gray-300 hover:text-[#0EA6E9]">Technology</a></li>
              <li><a href="#" className="text-gray-300 hover:text-[#0EA6E9]">Finance</a></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div className="space-y-4">
            <h3 className="text-[#0EA6E9] text-lg font-bold">Contact Us</h3>
            <ul className="space-y-2">
              <li className="text-gray-300">Email: support@newslens.com</li>
              <li className="text-gray-300">Phone: +1 (123) 456-7890</li>
              <li className="text-gray-300">Address: 123 News St, City, Country</li>
            </ul>
          </div>

          {/* Social Media */}
          <div className="space-y-4">
            <h3 className="text-[#0EA6E9] text-lg font-bold">Follow Us</h3>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-300 hover:text-[#0EA6E9]">
                <Facebook className="h-6 w-6" />
              </a>
              <a href="#" className="text-gray-300 hover:text-[#0EA6E9]">
                <Instagram className="h-6 w-6" />
              </a>
              <a href="#" className="text-gray-300 hover:text-[#0EA6E9]">
                <Linkedin className="h-6 w-6" />
              </a>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-800 mt-8 pt-4 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} NewsLens. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}