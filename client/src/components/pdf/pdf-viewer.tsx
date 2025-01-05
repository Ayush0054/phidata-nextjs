'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut, RotateCw } from 'lucide-react'

export function PDFViewer() {
  const [scale, setScale] = useState(1)
  const [page, setPage] = useState(1)
  const totalPages = 32

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-2 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={() => setScale(s => Math.min(s + 0.1, 2))}>
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" onClick={() => setScale(s => Math.max(s - 0.1, 0.5))}>
            <ZoomOut className="h-4 w-4" />
          </Button>
          <span className="text-sm text-muted-foreground">
            {Math.round(scale * 100)}%
          </span>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={() => setPage(p => Math.max(p - 1, 1))}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <span className="text-sm">
            Page {page} of {totalPages}
          </span>
          <Button variant="ghost" size="icon" onClick={() => setPage(p => Math.min(p + 1, totalPages))}>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
        <Button variant="ghost" size="icon">
          <RotateCw className="h-4 w-4" />
        </Button>
      </div>
      <div className="flex-1 overflow-auto p-4 ">
        <div 
          className="mx-auto bg-white rounded-lg shadow-lg h-[75vh]"
          style={{ 
            width: `${Math.min(850 * scale, window.innerWidth - 100)}px`,
            transform: `scale(${scale})`,
            transformOrigin: 'top center'
          }}
        >
          <div className=" h-full">
            {/* PDF content will be rendered here */}
            <div className="absolute inset-0 flex items-center justify-center text-muted-foreground h-full">
              PDF Content
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

