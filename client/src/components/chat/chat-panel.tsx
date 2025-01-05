'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Bot, Send } from 'lucide-react'

export function ChatPanel() {
  const [message, setMessage] = useState("")

  return (
    <div className="w-[400px] border-l flex flex-col bg-background">
      <div className="border-b">
        <Tabs defaultValue="chat" className="w-full">
          <TabsList className="w-full justify-start rounded-none border-b px-4">
            <TabsTrigger value="chat" className="rounded-none">Chat</TabsTrigger>
            <TabsTrigger value="summary" className="rounded-none">Summary</TabsTrigger>
            <TabsTrigger value="insights" className="rounded-none">Insights</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>
      <ScrollArea className="flex-1 p-4">
        <div className="flex gap-3 mb-4">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
            <Bot className="w-4 h-4 text-primary-foreground" />
          </div>
          <div className="flex-1">
            <p className="text-sm text-muted-foreground">
              Hello! I&apos;m your reading assistant. I can help you understand the document better.
              Feel free to ask any questions about the content.
            </p>
          </div>
        </div>
      </ScrollArea>
      <div className="border-t p-4">
        <div className="flex gap-2">
          <Input
            placeholder="Ask a question..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
          <Button size="icon">
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}

