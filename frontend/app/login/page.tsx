"use client";

import { useState } from "react";
import { LoginFormDemo } from "../signup/login"; // Correct import
import { BackgroundBeams } from "@/components/ui/background-beams";

export default function LoginPage() {
  const [email, setEmail] = useState("");

  return (
    <>
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

      {/* Login Form Centered */}
      <div className="flex justify-center items-center min-h-screen p-4">
        <LoginFormDemo />
      </div>
    </>
  );
}


  