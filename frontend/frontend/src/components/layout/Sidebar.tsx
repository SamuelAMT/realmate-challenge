import { useState } from "react";
import { Link } from "react-router-dom";
import { useConversations } from "@/hooks/useConversations";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { formatConversationTime, truncateText } from "@/lib/utils";
import { Search } from "lucide-react";

export function Sidebar() {
  const { conversations, isLoading } = useConversations();
  const [searchQuery, setSearchQuery] = useState("");

  const filteredConversations = conversations.filter(conv => {
    // In a real app, you'd search messages content too
    return conv.conversation_id.includes(searchQuery.toLowerCase());
  });

  return (
    <div className="w-full md:w-[350px] border-r border-gray-200 bg-white h-[calc(100vh-4rem)] flex flex-col">
      <div className="p-3 border-b border-gray-200">
        <div className="relative">
          <Search className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" />
          <Input
            placeholder="Search conversations"
            className="pl-9"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        {isLoading ? (
          Array(5).fill(0).map((_, i) => (
            <div key={i} className="flex items-center gap-3 p-3 border-b border-gray-100">
              <Skeleton className="h-12 w-12 rounded-full" />
              <div className="flex-1">
                <Skeleton className="h-4 w-24 mb-2" />
                <Skeleton className="h-3 w-40" />
              </div>
            </div>
          ))
        ) : filteredConversations.length > 0 ? (
          filteredConversations.map((conversation) => {
            const lastMessage = conversation.messages[conversation.messages.length - 1];
            return (
              <Link
                to={`/conversations/${conversation.conversation_id}`}
                key={conversation.conversation_id}
                className="flex items-center gap-3 p-3 border-b border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <Avatar>
                  <AvatarFallback>
                    {conversation.conversation_id.slice(-2).toUpperCase()}
                  </AvatarFallback>
                </Avatar>

                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-center">
                    <h3 className="font-medium text-sm">
                      Conversation #{conversation.conversation_id.slice(-4)}
                    </h3>
                    <span className="text-xs text-gray-500">
                      {formatConversationTime(conversation.updated_at)}
                    </span>
                  </div>

                  <div className="flex items-center gap-1">
                    <p className="text-sm text-gray-600 truncate">
                      {lastMessage ? truncateText(lastMessage.content, 35) : "No messages"}
                    </p>

                    <Badge
                      variant="outline"
                      className={
                        conversation.status === "OPEN"
                          ? "bg-green-100 text-green-800 border-green-200 ml-1"
                          : "bg-red-100 text-red-800 border-red-200 ml-1"
                      }
                    >
                      {conversation.status}
                    </Badge>
                  </div>
                </div>
              </Link>
            );
          })
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <p>No conversations found</p>
          </div>
        )}
      </div>
    </div>
  );
}