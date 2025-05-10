import { useState } from "react";
import type { FormEvent } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Paperclip, Send, Lock } from "lucide-react"; // Added Lock icon
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

interface MessageInputProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
  conversationStatus?: "OPEN" | "CLOSED";
}

export function MessageInput({
  onSendMessage,
  disabled = false,
  conversationStatus = "OPEN"
}: MessageInputProps) {
  const [message, setMessage] = useState("");
  const isClosed = conversationStatus === "CLOSED";

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (message.trim() && !disabled && !isClosed) {
      onSendMessage(message);
      setMessage("");
    }
  };

  // Visual feedback for closed conversation
  if (isClosed) {
    return (
      <div className="bg-white border-t border-gray-200 p-3 flex items-center space-x-2 sticky bottom-0 z-10">
        <div className="flex items-center justify-center w-full py-3 bg-gray-100 rounded text-gray-500">
          <Lock className="h-4 w-4 mr-2" />
          <span>This conversation is closed and no longer accepts messages</span>
        </div>
      </div>
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white border-t border-gray-200 p-3 flex items-center space-x-2 sticky bottom-0 z-10"
    >
      <Button
        type="button"
        variant="ghost"
        size="icon"
        disabled={disabled}
      >
        <Paperclip className="h-5 w-5" />
      </Button>

      <Input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message"
        className="flex-1"
        disabled={disabled}
      />

      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            type="submit"
            size="icon"
            disabled={!message.trim() || disabled}
            className="bg-green-600 hover:bg-green-700 text-white"
          >
            <Send className="h-4 w-4" />
          </Button>
        </TooltipTrigger>
        <TooltipContent>
          <p>Send message</p>
        </TooltipContent>
      </Tooltip>
    </form>
  );
}