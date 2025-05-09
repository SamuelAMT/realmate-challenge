import { useEffect, useRef } from "react";
import { Message } from "@/database/schema";
import { MessageItem } from "./MessageItem";
import { ScrollArea } from "@/components/ui/scroll-area";

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

export function MessageList({ messages, isLoading = false }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  if (isLoading) {
    return (
      <div className="message-list flex flex-col justify-center items-center">
        <div className="text-gray-500">Loading messages...</div>
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div className="message-list flex flex-col justify-center items-center">
        <div className="text-gray-500">No messages yet</div>
      </div>
    );
  }

  return (
    <ScrollArea className="message-list">
      {messages.map((message) => (
        <MessageItem key={message.message_id} message={message} />
      ))}
      <div ref={bottomRef} />
    </ScrollArea>
  );
}