import { useState, useEffect } from "react";
import type { Conversation } from "@/database/schema";
import { mockConversations } from "@/database/schema";
// import { fetchConversation } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

export function useConversation(conversationId: string) {
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    const loadConversation = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // For demo purposes, using mock data
        // In production, use the fetchConversation function
        // const data = await fetchConversation(conversationId);

        // Mock API delay
        await new Promise(resolve => setTimeout(resolve, 800));

        const data = mockConversations.find(
          conv => conv.conversation_id === conversationId
        );

        if (!data) {
          throw new Error("Conversation not found");
        }

        setConversation(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error("Failed to load conversation"));
        toast({
          title: "Error",
          description: "Failed to load conversation",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    loadConversation();
  }, [conversationId, toast]);

  const sendMessage = async (content: string) => {
    if (!conversation) return;

    const newMessage = {
      message_id: `temp-${Date.now()}`,
      direction: "SENT" as const,
      content,
      conversation_id: conversationId,
      timestamp: new Date().toISOString(),
    };

    // Optimistic update
    setConversation(prev => {
      if (!prev) return prev;
      return {
        ...prev,
        messages: [...prev.messages, newMessage],
      };
    });

    // In production, call API to send message
    // try {
    //   const sentMessage = await sendMessage(conversationId, content);
    //   // Update with server response if needed
    // } catch (err) {
    //   // Handle error, revert optimistic update
    //   toast({
    //     title: "Error",
    //     description: "Failed to send message",
    //     variant: "destructive",
    //   });
    //   setConversation(prev => {
    //     if (!prev) return prev;
    //     return {
    //       ...prev,
    //       messages: prev.messages.filter(msg => msg.message_id !== newMessage.message_id),
    //     };
    //   });
    // }
  };

  return {
    conversation,
    isLoading,
    error,
    sendMessage,
  };
}