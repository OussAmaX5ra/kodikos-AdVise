export default function LandingSection2() {
  return (
    <section className="bg-gray-50 py-20 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-black mb-4">How It Works</h2>
          <p className="text-gray-600 text-lg">
            Get started in minutes and see results immediately with our AI-powered optimization platform.
          </p>
        </div>

        {/* Dashboard Preview */}
        <div className="mb-20">
          <img
            src="/images/design-mode/section2.png"
            alt="Campaign Dashboard"
            className="w-full h-auto rounded-xl shadow-lg"
          />
        </div>
      </div>
    </section>
  )
}
