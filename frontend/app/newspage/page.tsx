"use client";

import { useState } from "react";
import { Sidebar } from "@/components/ui/slidebar"; // Correct import
import { BackgroundBeams } from "@/components/ui/background-beams";
import { SidebarDemo } from "../selectednews";

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
      <div>
        <SidebarDemo></SidebarDemo>
        </div>
    </>
  );
}
