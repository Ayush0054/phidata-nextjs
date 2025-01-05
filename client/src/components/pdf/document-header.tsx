import { Button } from "@/components/ui/button"
import { Info, Share, Star } from 'lucide-react'

export function DocumentHeader() {
  return (
    <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 items-center px-4 gap-4">
        <div className="flex-1">
          <h1 className="text-lg font-semibold">The Future is Now: Innovations in Technology and Science</h1>
          <p className="text-sm text-muted-foreground">
            Contributors: Svetoslav Nizhnichenkov, Rahul Nair, Elizabeth Daly
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon">
            <Star className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon">
            <Share className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon">
            <Info className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}

