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

// Mock data for development
export const mockConversations: Conversation[] = [
  {
    conversation_id: "conv-001",
    status: "OPEN",
    created_at: "2023-05-01T10:00:00Z",
    updated_at: "2023-05-01T14:30:00Z",
    messages: [
      {
        message_id: "msg-001",
        direction: "RECEIVED",
        content: "Hello! I'm interested in your product.",
        conversation_id: "conv-001",
        timestamp: "2023-05-01T10:00:00Z"
      },
      {
        message_id: "msg-002",
        direction: "SENT",
        content: "Hi there! Thanks for your interest. How may I help you today?",
        conversation_id: "conv-001",
        timestamp: "2023-05-01T10:05:00Z"
      },
      {
        message_id: "msg-003",
        direction: "RECEIVED",
        content: "I'd like to know more about pricing options.",
        conversation_id: "conv-001",
        timestamp: "2023-05-01T10:10:00Z"
      },
      {
        message_id: "msg-004",
        direction: "SENT",
        content: "Of course! We have several pricing tiers. Our basic package starts at $19.99/month and includes all essential features.",
        conversation_id: "conv-001",
        timestamp: "2023-05-01T10:15:00Z"
      }
    ]
  },
  {
    conversation_id: "conv-002",
    status: "CLOSED",
    created_at: "2023-04-28T09:00:00Z",
    updated_at: "2023-04-28T11:45:00Z",
    messages: [
      {
        message_id: "msg-005",
        direction: "RECEIVED",
        content: "Hi, I'm having trouble accessing my account.",
        conversation_id: "conv-002",
        timestamp: "2023-04-28T09:00:00Z"
      },
      {
        message_id: "msg-006",
        direction: "SENT",
        content: "I'm sorry to hear that. Could you please provide your username or email address?",
        conversation_id: "conv-002",
        timestamp: "2023-04-28T09:05:00Z"
      },
      {
        message_id: "msg-007",
        direction: "RECEIVED",
        content: "It's john.doe@example.com",
        conversation_id: "conv-002",
        timestamp: "2023-04-28T09:10:00Z"
      },
      {
        message_id: "msg-008",
        direction: "SENT",
        content: "Thank you. I've reset your password. You should receive an email with instructions shortly.",
        conversation_id: "conv-002",
        timestamp: "2023-04-28T09:15:00Z"
      },
      {
        message_id: "msg-009",
        direction: "RECEIVED",
        content: "Got it! Thanks for your help.",
        conversation_id: "conv-002",
        timestamp: "2023-04-28T09:30:00Z"
      },
      {
        message_id: "msg-010",
        direction: "SENT",
        content: "You're welcome! Let me know if you need anything else.",
        conversation_id: "conv-002",
        timestamp: "2023-04-28T09:35:00Z"
      }
    ]
  }
];