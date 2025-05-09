import { useParams } from "react-router-dom";
import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import { Footer } from "@/components/layout/Footer";
import { ConversationHeader } from "@/components/conversation/ConversationHeader";
import { MessageList } from "@/components/conversation/MessageList";
import { MessageInput } from "@/components/conversation/MessageInput";
import { useConversation } from "@/hooks/useConversation";

const ConversationPage = () => {
  const { id } = useParams<{ id: string }>();
  const { conversation, isLoading, error, sendMessage } = useConversation(id || "");

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <div className="flex flex-col md:flex-row flex-1">
        <div className="hidden md:block">
          <Sidebar />
        </div>

        <div className="flex-1 flex flex-col">
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
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default ConversationPage;
