'use client'

import { Upload, Save, Share2, RotateCcw } from 'lucide-react'

export default function ReportHeader() {
  return (
    <div className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-center gap-2">
      <button className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-1.5 px-3 font-medium flex items-center gap-2 transition text-sm">
        <Upload className="w-3.5 h-3.5" />
        Upload Data
      </button>
      <button className="text-gray-600 hover:text-gray-900 flex items-center gap-2 transition text-sm">
        <Save className="w-3.5 h-3.5" />
        Save
      </button>
      <button className="text-gray-600 hover:text-gray-900 flex items-center gap-2 transition text-sm">
        <Share2 className="w-3.5 h-3.5" />
        Share
      </button>

      <div className="flex items-center gap-2 ml-4">
        <button className="text-gray-600 hover:text-gray-900 transition">
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
        <button className="text-gray-600 hover:text-gray-900 transition">
          <RotateCcw className="w-3.5 h-3.5 transform scale-x-[-1]" />
        </button>
      </div>
    </div>
  )
}
