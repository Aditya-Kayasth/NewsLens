"use client";
import React from "react";

interface NewsCardProps {
  category: string;
}

const NewsCard: React.FC<NewsCardProps> = ({ category }) => {
  return (
    <div className="md:col-span-1 bg-gray-900 rounded-lg p-6 h-[500px] flex flex-col justify-center hover:shadow-[20px_20px_20px_-5px_rgba(14,166,233,0.3)] hover:shadow-[#0EA6E9]/30 transition-shadow duration-200">
      <h2 className="text-2xl font-bold mb-2 hover:text-[#0EA6E9] transition-colors duration-200">
        {category} News: Major Event Impacting the Industry
      </h2>
      <p className="text-gray-300 mb-3 hover:text-gray-100 transition-colors duration-200">
        Stay updated with the latest breaking news and developments in {category}.
      </p>
      <time className="text-sm text-gray-400 hover:text-gray-200 transition-colors duration-200">
        Sep 09, 2024
      </time>
    </div>
  );
};

export default NewsCard;
