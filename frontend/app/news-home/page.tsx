"use client"; // Ensures hooks work in Next.js App Router

import { useEffect, useState } from "react";
import { Search } from "lucide-react";
import { Input2 } from "../../components/ui/input2";
import { Footer } from "../../components/ui/footer";
import MainNav from "../main-nav/main-nav";
import TopNav from "../top-nav/top-nav";
import ThemeSwitcher from "../../components/ui/theme-switcher";
import NewsPaperImage from "../../components/ui/NewsPaper.png";
import NewsCard from "../../components/ui/NewsCard"; // Import NewsCard component

export default function NewsPage() {
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);

  // Fetch user-selected categories from localStorage
  useEffect(() => {
    const storedPreferences = localStorage.getItem("newsPreferences");
    if (storedPreferences) {
      setSelectedCategories(JSON.parse(storedPreferences));
    }
  }, []);

  return (
    <div className="min-h-screen text-white bg-background">
      <TopNav />

      <header className="border-b border-gray-800">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <h1 className="text-[#0EA6E9] text-3xl font-bold hover:text-[#809fff] transition-colors duration-200">
                NewsLens
              </h1>
              <img
                src={NewsPaperImage.src}
                alt="NewsPaper Logo"
                className="w-21 h-20 rounded-full hover:scale-200 transition-transform duration-200"
              />
            </div>

            <div className="flex items-center gap-4">
              <div className="relative w-[300px]">
                <Input2
                  type="search"
                  placeholder="Search anything"
                  className="bg-gray-900/50 border border-black pl-4 pr-10 text-black placeholder-gray-500 shadow-md shadow-gray-500/50 focus:ring-2 focus:ring-[#0EA6E9] rounded-lg hover:shadow-[20px_20px_20px_-5px_rgba(14,166,233,0.3)] hover:shadow-[#0EA6E9]/30 transition-shadow duration-200"
                />
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 hover:text-[#0EA6E9] transition-colors duration-300" />
              </div>
              <ThemeSwitcher />
            </div>
          </div>

          <MainNav />
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Show only the news categories the user selected */}
        {selectedCategories.length > 0 ? (
          selectedCategories.map((category) => (
            <section key={category}>
              <div className="mb-6">
                <span className="inline-block px-3 py-1 bg-[#0EA6E9] rounded-full text-sm hover:bg-[#809fff] transition-colors duration-200">
                  {category}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <NewsCard category={category} />
              </div>
              <br />
            </section>
          ))
        ) : (
          <p className="text-center text-gray-400">No preferences selected. Please go back and choose categories.</p>
        )}
      </main>

      <Footer />
    </div>
  );
}
