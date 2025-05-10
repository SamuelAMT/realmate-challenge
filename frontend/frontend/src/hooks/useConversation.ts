import { useState, useEffect } from "react";
import type { Conversation, Message } from "@/database/schema";
import {
  fetchConversation,
  sendMessage as apiSendMessage,
  closeConversation as apiCloseConversation,
} from "@/lib/api";
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
    if (!conversationId || !conversation) return;

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

    try {
      const sentMessage = await apiSendMessage(conversationId, content);

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

  const closeConversation = async () => {
    if (!conversation) return;

    try {
      const closedConversation = await apiCloseConversation(conversationId);
      setConversation(closedConversation);

      toast({
        title: "Success",
        description: "Conversation closed successfully",
      });

      return closedConversation;
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to close conversation",
        variant: "destructive",
      });
      throw err;
    }
  };

  return {
    conversation,
    isLoading,
    error,
    sendMessage,
    closeConversation,
  };
}
