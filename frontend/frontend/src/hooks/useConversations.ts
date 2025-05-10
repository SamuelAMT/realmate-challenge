import { useState, useEffect } from "react";
import type { Conversation } from "@/database/schema";
import { fetchConversations } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

export function useConversations() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    const loadConversations = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Use the actual API endpoint
        const data = await fetchConversations();
        setConversations(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error("Failed to load conversations"));
        toast({
          title: "Error",
          description: "Failed to load conversations",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    loadConversations();
  }, [toast]);

  return {
    conversations,
    isLoading,
    error,
  };
}