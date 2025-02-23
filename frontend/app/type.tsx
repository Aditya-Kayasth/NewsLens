"use client";
import { TypewriterEffectSmooth } from "@/components/ui/typewriter-effect";
import { useRouter } from "next/navigation"; // Import useRouter for navigation

export function TypewriterEffectSmoothDemo() {
  const router = useRouter(); // Initialize Next.js router

  const words = [
    {
      text: "Uncover News",
      className: "text-white",
    },
    {
      text: "That Moves",
      className: "text-white",
    },
    {
      text: "You",
      className: "text-white",
    },
    {
      text: "with",
      className: "text-white",
    },
    {
      text: "InsightPlus.",
      className: "text-sky-500 dark:text-white italic font-bold font-times",
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center h-[40rem]">
      <p className="text-sky-200 text-sm sm:text-base">
        The Quest for Clarity Begins here...
      </p>

      <TypewriterEffectSmooth words={words} />

      {/* Buttons for Sign Up & Login */}
      <div className="mt-6 flex flex-col md:flex-row space-y-6 md:space-y-0 md:space-x-8">
        {/* Sign Up Button */}
        <button
          onClick={() => {
            console.log("Redirecting to /signup...");
            router.push("/signup");
          }}
          className="w-40 h-10 rounded-xl bg-sky-500 border dark:border-white border-transparent text-white text-sm font-[Times_New_Roman] transition-all duration-300 ease-in-out shadow-lg hover:shadow-2xl hover:translate-y-[-3px] hover:scale-105"
        >
          <b>Sign Up</b>
        </button>

        {/* Login Button */}
        <button
          onClick={() => {
            console.log("Redirecting to /login...");
            router.push("/login");
          }}
          className="w-40 h-10 rounded-xl bg-white text-black border border-black text-sm font-[Times_New_Roman] transition-all duration-300 ease-in-out shadow-lg hover:shadow-2xl hover:translate-y-[-3px] hover:scale-105"
        >
          <b>Login</b>
        </button>
      </div>
    </div>
  );
}


