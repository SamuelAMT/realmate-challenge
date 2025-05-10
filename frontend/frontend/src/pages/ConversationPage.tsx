import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import { Footer } from "@/components/layout/Footer";
import { ConversationHeader } from "@/components/conversation/ConversationHeader";
import { MessageList } from "@/components/conversation/MessageList";
import { MessageInput } from "@/components/conversation/MessageInput";
import { useConversation } from "@/hooks/useConversation";
import { Button } from "@/components/ui/button";
import { createConversation } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

const ConversationPage = () => {
  const { id } = useParams<{ id: string }>();
  const { conversation, isLoading, error, sendMessage } = useConversation(id || "");
  const [isCreating, setIsCreating] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleCreateConversation = async () => {
    try {
      setIsCreating(true);
      const newConversation = await createConversation();
      toast({
        title: "Success",
        description: "New conversation created",
      });
      navigate(`/conversations/${newConversation.conversation_id}`);
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to create conversation",
        variant: "destructive",
      });
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <div className="flex flex-col md:flex-row flex-1">
        <div className="hidden md:block">
          <Sidebar />
        </div>

        <div className="flex-1 flex flex-col">
          {id ? (
            <>
              <ConversationHeader conversation={conversation || undefined} isLoading={isLoading} />

              {error ? (
                <div className="flex-1 flex items-center justify-center">
                  <div className="text-center">
                    <h3 className="text-xl font-bold text-red-500">Error</h3>
                    <p className="text-gray-600 mt-2">{error.message}</p>
                  </div>
                </div>
              ) : (
                <>
                  <MessageList
                    messages={conversation?.messages || []}
                    isLoading={isLoading}
                  />
                  <MessageInput
                    onSendMessage={sendMessage}
                    disabled={isLoading || !conversation}
                  />
                </>
              )}
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <h3 className="text-xl font-bold">No Conversation Selected</h3>
                <p className="text-gray-600 mt-2">Select a conversation from the sidebar or create a new one</p>
                <Button
                  onClick={handleCreateConversation}
                  disabled={isCreating}
                  className="mt-4"
                >
                  {isCreating ? "Creating..." : "Create New Conversation"}
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default ConversationPage;