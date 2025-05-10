import { createConversation, sendMessage } from "@/lib/api";

// Sample conversation data
const conversationData = [
  {
    messages: [
      { content: "Hello! I'm interested in your product.", direction: "RECEIVED" },
      { content: "Hi there! Thanks for your interest. How may I help you today?", direction: "SENT" },
      { content: "I'd like to know more about pricing options.", direction: "RECEIVED" },
      { content: "Of course! We have several pricing tiers. Our basic package starts at $19.99/month and includes all essential features.", direction: "SENT" }
    ]
  },
  {
    messages: [
      { content: "Hi, I'm having trouble accessing my account.", direction: "RECEIVED" },
      { content: "I'm sorry to hear that. Could you please provide your username or email address?", direction: "SENT" },
      { content: "It's john.doe@example.com", direction: "RECEIVED" },
      { content: "Thank you. I've reset your password. You should receive an email with instructions shortly.", direction: "SENT" },
      { content: "Got it! Thanks for your help.", direction: "RECEIVED" },
      { content: "You're welcome! Let me know if you need anything else.", direction: "SENT" }
    ]
  },
  {
    messages: [
      { content: "Hello, I've been charged twice for my subscription this month.", direction: "RECEIVED" },
      { content: "I apologize for the inconvenience. Let me look into this for you.", direction: "SENT" },
      { content: "Thank you. My account number is 12345.", direction: "RECEIVED" },
      { content: "I've checked your account and confirmed the double charge. I've processed a refund for the duplicate payment. It should appear in your account within 3-5 business days.", direction: "SENT" },
      { content: "Perfect, thank you for resolving this so quickly!", direction: "RECEIVED" },
      { content: "You're welcome! We appreciate your patience. Is there anything else I can help you with today?", direction: "SENT" },
      { content: "No, that's all. Have a great day!", direction: "RECEIVED" },
      { content: "You too! Don't hesitate to reach out if you need anything else.", direction: "SENT" }
    ]
  }
];

// Function to create conversations with messages
async function populateTestData() {
  try {
    console.log("Starting to populate test data...");

    for (let i = 0; i < conversationData.length; i++) {
      console.log(`Creating conversation ${i+1}/${conversationData.length}...`);

      // Create a new conversation
      const conversation = await createConversation();
      console.log(`Created conversation with ID: ${conversation.conversation_id}`);

      // Add messages to the conversation
      for (let j = 0; j < conversationData[i].messages.length; j++) {
        const message = conversationData[i].messages[j];
        console.log(`Sending message ${j+1}/${conversationData[i].messages.length}...`);

        // For "RECEIVED" messages, we'll use the webhook endpoint in a real scenario
        // For now, let's just use the regular sendMessage for demo purposes
        if (message.direction === "SENT") {
          await sendMessage(conversation.conversation_id, message.content);
        } else {
          // In a real application, you'd use the webhook endpoint
          // For now, we'll simulate this with the same endpoint
          await sendMessage(conversation.conversation_id, message.content);
        }

        // Add a small delay between messages to simulate a real conversation
        await new Promise(resolve => setTimeout(resolve, 500));
      }

      console.log(`Completed conversation ${i+1}`);
    }

    console.log("Test data population complete!");
  } catch (error) {
    console.error("Error populating test data:", error);
  }
}

// Run the function
populateTestData();