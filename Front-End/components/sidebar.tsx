'use client'

import { useState } from 'react'
import { BarChart3, FileText, Brain, CreditCard, TrendingUp } from 'lucide-react'
import Image from 'next/image'

interface SidebarProps {
  currentPage: string
  onPageChange: (page: string) => void
}

export default function Sidebar({ currentPage, onPageChange }: SidebarProps) {
  const [expanded, setExpanded] = useState(false)

  const menuItems = [
    { id: 'dashboard', icon: BarChart3, label: 'Dashboard', color: 'text-blue-600' },
    { id: 'report', icon: FileText, label: 'Report', color: 'text-purple-600' },
    { id: 'ai', icon: Brain, label: 'AI Advisor', color: 'text-indigo-600' },
    { id: 'accounts', icon: CreditCard, label: 'Accounts', color: 'text-green-600' },
    { id: 'campaign', icon: TrendingUp, label: 'Campaign', color: 'text-orange-600' },
  ]

  return (
    <aside
      className={`fixed left-0 top-0 h-screen bg-white border-r border-gray-200 transition-all duration-300 ease-in-out z-50 ${
        expanded ? 'w-64' : 'w-20'
      }`}
      onMouseEnter={() => setExpanded(true)}
      onMouseLeave={() => setExpanded(false)}
    >
      <div className="flex flex-col items-center justify-start h-full p-4 gap-8">
        {/* Logo */}
        <button
          onClick={() => window.location.href = '/'}
          className="flex items-center justify-center rounded-lg overflow-hidden w-12 h-12 hover:opacity-80 transition-opacity cursor-pointer"
        >
          <Image
            src="/images/design-mode/logo.PNG.png"
            alt="Logo"
            width={48}
            height={48}
            priority
          />
        </button>

        {/* Navigation Items */}
        <nav className="flex flex-col gap-4 w-full flex-1">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = currentPage === item.id

            return (
              <button
                key={item.id}
                onClick={() => onPageChange(item.id)}
                className={`flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-300 whitespace-nowrap ${
                  isActive
                    ? 'bg-gray-100 border-l-4 border-blue-600'
                    : 'hover:bg-gray-50'
                }`}
              >
                <Icon
                  className={`w-6 h-6 flex-shrink-0 transition-colors duration-300 ${
                    isActive ? 'text-blue-600' : 'text-gray-600'
                  }`}
                />
                {expanded && (
                  <span className={`text-sm font-medium transition-opacity duration-300 ${
                    isActive ? 'text-gray-900' : 'text-gray-700'
                  }`}>
                    {item.label}
                  </span>
                )}
              </button>
            )
          })}
          
          {/* Profile button at bottom */}
          <button
            onClick={() => onPageChange('profile')}
            className={`mt-auto flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-300 whitespace-nowrap ${
              currentPage === 'profile'
                ? 'bg-gray-100 border-l-4 border-blue-600'
                : 'hover:bg-gray-50'
            }`}
          >
            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center text-gray-700 font-bold text-xs flex-shrink-0">
              U
            </div>
            {expanded && (
              <span className={`text-sm font-medium transition-opacity duration-300 ${
                currentPage === 'profile' ? 'text-gray-900' : 'text-gray-700'
              }`}>
                Profile
              </span>
            )}
          </button>
        </nav>
      </div>
    </aside>
  )
}
