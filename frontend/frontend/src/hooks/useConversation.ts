import { useState, useEffect } from "react";
import type { Conversation, Message } from "@/database/schema";
import { fetchConversation, sendMessage as apiSendMessage } from "@/lib/api";
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

        // Use the actual API endpoint
        const data = await fetchConversation(conversationId);
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

    if (conversationId) {
      loadConversation();
    }
  }, [conversationId, toast]);

  const sendMessage = async (content: string) => {
    if (!conversation) return;

    const tempMessage: Message = {
      message_id: `temp-${Date.now()}`,
      direction: "SENT",
      content,
      conversation_id: conversationId,
      timestamp: new Date().toISOString(),
    };

    // Optimistic update
    setConversation(prev => {
      if (!prev) return prev;
      return {
        ...prev,
        messages: [...prev.messages, tempMessage],
      };
    });

    // Call the API to send the message
    try {
      const sentMessage = await apiSendMessage(conversationId, content);

      // Replace the temporary message with the real one from the server
      setConversation(prev => {
        if (!prev) return prev;
        return {
          ...prev,
          messages: prev.messages.map(msg =>
            msg.message_id === tempMessage.message_id ? sentMessage : msg
          ),
        };
      });
    } catch (err) {
      // Handle error, revert optimistic update
      toast({
        title: "Error",
        description: "Failed to send message",
        variant: "destructive",
      });

      setConversation(prev => {
        if (!prev) return prev;
        return {
          ...prev,
          messages: prev.messages.filter(msg => msg.message_id !== tempMessage.message_id),
        };
      });
    }
  };

  return {
    conversation,
    isLoading,
    error,
    sendMessage,
  };
}