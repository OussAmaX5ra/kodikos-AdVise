'use client'

import { useState } from 'react'
import Sidebar from '@/components/sidebar'
import DashboardPage from '@/pages/dashboard'
import ReportPage from '@/pages/report'
import AIAdvisorPage from '@/pages/ai-advisor'
import AccountsPage from '@/pages/accounts'
import CampaignPage from '@/pages/campaign'
import ProfilePage from '@/pages/profile'

export default function DashboardLayout() {
  const [currentPage, setCurrentPage] = useState('dashboard')

  const renderPage = () => {
    switch (currentPage) {
      case 'report':
        return <ReportPage />
      case 'dashboard':
        return <DashboardPage />
      case 'ai':
        return <AIAdvisorPage />
      case 'accounts':
        return <AccountsPage />
      case 'campaign':
        return <CampaignPage />
      case 'profile':
        return <ProfilePage />
      default:
        return <DashboardPage />
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar currentPage={currentPage} onPageChange={setCurrentPage} />
      <main className="flex-1 overflow-auto">
        {renderPage()}
      </main>
    </div>
  )
}
