'use client'

import LandingNavbar from '@/components/landing-navbar'
import LandingSection1 from '@/components/landing-section1'
import LandingSection2 from '@/components/landing-section2'
import LandingSection3 from '@/components/landing-section3'
import LandingFooter from '@/components/landing-footer'

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <LandingNavbar />
      <LandingSection1 />
      <LandingSection2 />
      <LandingSection3 />
      <LandingFooter />
    </div>
  )
}
