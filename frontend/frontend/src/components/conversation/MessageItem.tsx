import { Message } from "@/database/schema";
import { cn, formatMessageTime } from "@/lib/utils";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Check } from "lucide-react";

interface MessageItemProps {
  message: Message;
  animate?: boolean;
}

export function MessageItem({ message, animate = false }: MessageItemProps) {
  const isSent = message.direction === "SENT";
  const time = formatMessageTime(message.timestamp);

  return (
    <div
      className={cn(
        "flex items-end mb-2",
        isSent ? "justify-end" : "justify-start",
        animate && "animate-message-in"
      )}
    >
      <div
        className={cn(
          "message-bubble",
          isSent ? "message-sent" : "message-received"
        )}
      >
        <p className="text-sm">{message.content}</p>
        <div className="flex items-center justify-end gap-1 mt-1">
          <span className="text-xs text-gray-500">{time}</span>
          {isSent && (
            <Check className="h-3 w-3 text-gray-500" />
          )}
        </div>
      </div>
    </div>
  );
}