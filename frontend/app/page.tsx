"use client"; // Ensures hooks work in Next.js App Router

import { useRouter } from "next/navigation";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { FloatingNavDemo } from "./nav";
import { TypewriterEffectSmoothDemo } from "./type";
import { StickyScrollRevealDemo } from "./scroll";

// Button Component for Sign Up and Login
function NavigateButton({ label, route, bgColor, textColor, borderColor }) {
  const router = useRouter(); // Initialize Next.js router

  const handleClick = () => {
    console.log(`✅ ${label} button clicked! Redirecting to ${route}...`);
    router.push(route); // Navigate to the specified route
  };

  return (
    <button
      onClick={handleClick}
      className={`w-40 h-10 rounded-xl ${bgColor} ${textColor} ${borderColor} text-sm shadow-lg hover:scale-105 transition transform font-times border-2`}
    >
      <b>{label}</b>
    </button>
  );
}

// Home Page Component
export default function Home() {
  return (
    <>
      {/* Floating Navbar */}
      <div className="fixed top-0 left-0 w-full z-50">
        <FloatingNavDemo />
      </div>
      <TypewriterEffectSmoothDemo />

      {/* Background */}
      <div
        style={{
          backgroundColor: "#1b1f24",
          position: "fixed",
          zIndex: -1,
          top: 0,
          left: 0,
          width: "100vw",
          height: "100vh",
        }}
      >
        <BackgroundBeams />
      </div>

      {/* About Section */}
      <div id="about">
        <h1
          style={{
            color: "white",
            textAlign: "center",
            fontSize: "40px",
            fontFamily: "sans-serif",
          }}
        >
          <b>About Us 🤝</b>
        </h1>
        <StickyScrollRevealDemo />
      </div>

      {/* Contact Form */}
      <div
        className="w-[24rem] mx-auto bg-white dark:bg-neutral-900 shadow-lg rounded-2xl p-6 space-y-6 mb-10"
        id="contact"
      >
        <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mt-4">
          Contact Me 📩
        </h2>
        <p className="text-neutral-600 dark:text-neutral-400 text-center">
          Feel free to reach out by filling the form below.
        </p>

        <div className="space-y-4 flex flex-col items-center">
          <input
            type="text"
            placeholder="Your Name"
            className="w-3/4 px-4 py-2 border border-gray-300 dark:border-neutral-700 rounded-lg focus:ring-2 focus:ring-blue-500 bg-transparent text-gray-900 dark:text-white"
          />
          <input
            type="email"
            placeholder="Your Email"
            className="w-3/4 px-4 py-2 border border-gray-300 dark:border-neutral-700 rounded-lg focus:ring-2 focus:ring-blue-500 bg-transparent text-gray-900 dark:text-white"
          />
          <textarea
            placeholder="Your Message"
            className="w-3/4 h-24 px-4 py-2 border border-gray-300 dark:border-neutral-700 rounded-lg focus:ring-2 focus:ring-blue-500 bg-transparent text-gray-900 dark:text-white"
          />
          <button className="w-3/4 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition text-center">
            Send
          </button>
        </div>
      </div>

      {/* Buttons for Sign Up & Login */}
      

      {/* Footer */}
      <div className="w-full py-3 flex flex-col items-center justify-center bg-gradient-to-r from-gray-800 to-gray-900 text-white rounded-t-xl mt-10">
        <p className="text-sm font-semibold">© {new Date().getFullYear()} InsightPlus</p>
        <p className="text-xs opacity-75">
          In a world full of biased perspectives, we deliver actual happenings!
        </p>
      </div>
    </>
  );
}
