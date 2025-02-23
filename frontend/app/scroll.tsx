"use client";
import React from "react";
import { StickyScroll } from "@/components/ui/sticky-scroll-reveal";
import Image from "next/image";

const content = [
  {
    title: "AI-Powered Truth Verification",
    description:
      "At InsightPlus, our advanced AI technology scans over 150,000 sources to verify the authenticity of every news story. By eliminating human bias, we ensure that you receive unbiased and accurate information. Our commitment to truth is unwavering, and our AI-driven approach guarantees that every article you read is thoroughly vetted and reliable. Experience news as it should be—honest and transparent.",
    content: (
      <div className="h-full w-full bg-[linear-gradient(to_bottom_right,var(--cyan-500),var(--emerald-500))] flex items-center justify-center text-white">
        AI-Powered Truth Verification
      </div>
    ),
  },
  {
    title: "Real-Time, Personalized News Updates",
    description:
      "Stay informed with real-time news updates tailored just for you. Our AI learns from your preferences and activity to curate a personalized news feed that reflects your interests. Whether you're passionate about global events, technology innovations, or local happenings, our platform delivers the news that matters most to you, as it happens. No more sifting through irrelevant content—just pure, personalized insights.",
    content: (
      <div className="h-full w-full  flex items-center justify-center text-white">
        <Image
          src="/img.png"
          width={400}
          height={400}
          className="h-full w-full object-cover"
          alt="linear board demo"
        />
      </div>
    ),
  },
  {
    title: "Engage and Interact with Our Community",
    description:
      "Join a thriving community of readers and engage in lively discussions about the news that impacts your world. Our platform encourages open dialogue, allowing you to share your thoughts, ask questions, and flag any inaccuracies you encounter. Together, we can foster a collaborative environment where diverse perspectives are valued, and the truth is collectively upheld. Your voice matters, and our community is here to listen.",
    
  },
  {
    title: "Seamless, Bias-Free News Experience",
    description:
      "Experience a seamless news journey free from human interference and bias. Our AI-driven platform ensures that every story is presented fairly and accurately, without the influence of personal opinions. With the ability to flag incorrect information and engage in discussions, you become an active participant in maintaining the integrity of our news. Enjoy a smooth, unbiased news experience that keeps you informed and empowered.",
    
  },
];
export function StickyScrollRevealDemo() {
  return (
    <div className="p-10">
      <StickyScroll content={content} />
    </div>
  );
}
