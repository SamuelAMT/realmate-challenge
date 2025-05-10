export interface Message {
  message_id: string;
  direction: 'SENT' | 'RECEIVED';
  content: string;
  conversation_id: string;
  timestamp: string;
}

export interface Conversation {
  conversation_id: string;
  status: 'OPEN' | 'CLOSED';
  created_at: string;
  updated_at: string;
  messages: Message[];
}