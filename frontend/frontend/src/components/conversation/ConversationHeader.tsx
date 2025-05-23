import type { Conversation } from "@/database/schema";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { ArrowLeft, MoreVertical, Phone, VideoIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

interface ConversationHeaderProps {
  conversation?: Conversation;
  isLoading?: boolean;
  onClose?: () => Promise<void>;
}

export function ConversationHeader({conversation, isLoading = false, onClose }: ConversationHeaderProps) {
  const navigate = useNavigate();

  const handleClose = async () => {
    if (window.confirm("Are you sure you want to close this conversation?")) {
      try {
        await onClose?.();
      } catch (error) {
        console.error("Failed to close conversation:", error);
      }
    }
  };

  return (
    <div className="bg-white border-b border-gray-200 p-3 flex items-center justify-between sticky top-0 z-10">
      <div className="flex items-center space-x-3">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => navigate("/")}
        >
          <ArrowLeft className="h-5 w-5" />
        </Button>

        <Avatar>
          <AvatarFallback>
            {isLoading ? "..." : "C"}
          </AvatarFallback>
        </Avatar>

        <div>
          <h2 className="font-medium">
            {isLoading ? "Loading..." : `Conversation #${conversation?.conversation_id.slice(-4)}`}
          </h2>
          {conversation && (
            <Badge
              variant="outline"
              className={cn(
                "text-xs",
                conversation.status === "OPEN"
                  ? "bg-green-100 text-green-800 border-green-200"
                  : "bg-red-100 text-red-800 border-red-200"
              )}
            >
              {conversation.status}
            </Badge>
          )}
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <Button variant="ghost" size="icon">
          <Phone className="h-5 w-5" />
        </Button>
        <Button variant="ghost" size="icon">
          <VideoIcon className="h-5 w-5" />
        </Button>
        <Button variant="ghost" size="icon">
          <MoreVertical className="h-5 w-5" />
        </Button>

        {conversation?.status === "OPEN" && onClose && (
        <Button
          variant="outline"
          onClick={handleClose}
          disabled={isLoading}
          className="text-red-600 hover:text-red-700 hover:bg-red-50"
        >
          Close Conversation
        </Button>
      )}
      </div>
    </div>
  );
}
