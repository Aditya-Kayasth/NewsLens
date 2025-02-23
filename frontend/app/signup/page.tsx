"use client";

import { useState } from "react";
import { SignupFormDemo } from "../signup";
import { BackgroundBeams } from "@/components/ui/background-beams";

export default function SignupPage() {
  const [email, setEmail] = useState("");

  return (
    <>
    <div style={{
          backgroundColor: "#1b1f24",
          position: "fixed",
          zIndex: -1,
          top: 0,
          left: 0,
          width: "100vw",
          height: "100vh",
        }}><BackgroundBeams/></div>
    
    <div style={{
        marginTop:"10px",
    }}>
      <SignupFormDemo/>
    </div></>
    
  );
}

  
