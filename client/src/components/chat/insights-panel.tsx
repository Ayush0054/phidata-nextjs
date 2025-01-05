'use client'

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"

export function InsightPanel() {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Context & Insights</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="context">
          <TabsList className="grid w-full grid-cols-3 mb-4">
            <TabsTrigger value="context">Context</TabsTrigger>
            <TabsTrigger value="summary">Summary</TabsTrigger>
            <TabsTrigger value="insights">Insights</TabsTrigger>
          </TabsList>
          <TabsContent value="context">
            <ScrollArea className="h-[500px]">
              <div className="space-y-4">
                <h3 className="font-semibold">Selected Text Context</h3>
                <p className="text-sm text-muted-foreground">
                  Select text in the PDF viewer to see its context and analysis here.
                </p>
              </div>
            </ScrollArea>
          </TabsContent>
          <TabsContent value="summary">
            <ScrollArea className="h-[500px]">
              <div className="space-y-4">
                <h3 className="font-semibold">Document Summary</h3>
                <p className="text-sm text-muted-foreground">
                  A comprehensive summary of the document will appear here.
                </p>
              </div>
            </ScrollArea>
          </TabsContent>
          <TabsContent value="insights">
            <ScrollArea className="h-[500px]">
              <div className="space-y-4">
                <h3 className="font-semibold">Key Insights</h3>
                <p className="text-sm text-muted-foreground">
                  AI-generated insights and analysis will be displayed here.
                </p>
              </div>
            </ScrollArea>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}

