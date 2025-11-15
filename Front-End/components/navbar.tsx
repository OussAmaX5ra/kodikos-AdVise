'use client'

import { Menu, Search, Sun, Moon, RotateCcw, Bell } from 'lucide-react'
import { useTheme } from '@/components/theme-provider'

function Navbar() {
  const { isDark, toggleTheme } = useTheme()

  return (
    <nav className="bg-white dark:bg-[#181C26] border-b border-gray-200 dark:border-[#2A3142] px-6 py-3 flex items-center justify-between transition-colors">
      <div className="flex items-center gap-4">
        <Menu className="w-5 h-5 text-gray-600 dark:text-gray-300 cursor-pointer hover:text-gray-900 dark:hover:text-white transition" />
      </div>

      <div className="flex-1 flex items-center justify-center">
        <div className="relative w-80">
          <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500" />
          <input
            type="text"
            placeholder="Search"
            className="w-full bg-gray-50 dark:bg-[#0F131A] border border-gray-200 dark:border-[#2A3142] rounded-lg pl-10 pr-4 py-2 text-sm placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
          />
          <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-xs text-gray-400 dark:text-gray-500">⌘ /</span>
        </div>
      </div>

      <div className="flex items-center gap-5">
        <button 
          onClick={toggleTheme}
          className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition"
          title="Toggle dark mode"
        >
          {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
        <button className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition">
          <RotateCcw className="w-4 h-4" />
        </button>
        <button className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition">
          <Bell className="w-4 h-4" />
        </button>
      </div>
    </nav>
  )
}

export default Navbar
