import { useState } from "react";
import type { FormEvent } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Paperclip, Send } from "lucide-react";

interface MessageInputProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
}

export function MessageInput({ onSendMessage, disabled = false }: MessageInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage("");
    }
  };

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

      <Button
        type="submit"
        size="icon"
        disabled={!message.trim() || disabled}
        className="bg-whatsapp-green hover:bg-whatsapp-darkGreen"
      >
        <Send className="h-4 w-4" />
      </Button>
    </form>
  );
}